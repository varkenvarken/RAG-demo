# tweak to ensure pysqlite3 is used instead of sqlite3, because chroma requires sqlite 3.35
# we pinned the packages to chromadb==1.0.7  and pysqlite3-binary==0.5.4
import codecs
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


from sqlite3 import connect

from chromadb import HttpClient
from dataclasses import dataclass



# Initialize DB
conn = connect("/data/descriptions.db")  # Or your actual DB connection

# initialize chroma client
chromaclient = HttpClient(host="chromadb", port=8000)
collection = chromaclient.get_or_create_collection("book_descriptions")


# Ensure the Description table exists
def ensure_module_table_exists():
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS Module (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(name)
            )
            """
    )


def add_module_with_rag(name, description):
    # Add to SQL database
    result = conn.execute(
        """INSERT INTO Module (name, description)
                VALUES (:name, :description)
                ON CONFLICT(name) DO UPDATE SET description = excluded.description
                RETURNING id""",
        {"name": name, "description": description}
    )

    row = result.fetchone()
    doc_id = str(row[0])
    collection.add(documents=[description], metadatas=[
        {"name": name}], ids=[doc_id])


@dataclass
class Result:
    id: str
    metadata: dict
    document: str
    distance: float

def initialize():
    # Initialize the database and collection
    ensure_module_table_exists()
    
    from csv import DictReader
    # Read the CSV file and add each row to the database
    with open("RPA-ProDev-ModuleDEscriptions.csv", "r", encoding="latin_1") as f:
        DictReader = DictReader(f)
        for row in DictReader:
            # print(list(row.keys()))
            add_module_with_rag(row["title"], row["content"])

# === Query function ===


def query_modules(natural_query: str, k: int = 5):
    # Embed and search
    results = collection.query(query_texts=[natural_query], n_results=k)

    for i in range(k):
        yield Result(
            id=results["ids"][0][i],
            metadata=results["metadatas"][0][i],
            document=results["documents"][0][i],
            distance=results["distances"][0][i]
        )


if __name__ == "__main__":
    initialize()

    from sys import argv
    for result in query_modules(" ".join(argv[1:]), 5):
        print(result.id, result.distance, result.metadata["title"])
