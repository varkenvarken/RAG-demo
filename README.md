# RAG-Demo

This project demonstrates a **Retrieval-Augmented Generation (RAG)** system. It includes a backend server that processes natural language queries and retrieves relevant information from a database, as well as a frontend interface for interacting with the system.

## Features

- **Backend**:
  - A Python HTTP server (`server.py`) that handles:
    - Serving a static HTML file (`index.html`).
    - Processing POST requests to the `/question` endpoint to query a database.
  - Integration with a ChromaDB instance for embedding-based retrieval.
  - Query results include metadata, document content, and similarity scores.

- **Frontend**:
  - A simple HTML interface (`index.html`) where users can:
    - Enter a question in a text box.
    - View query results as a list of items.
    - Click on an item to view its detailed description in a popup panel.

## Project Structure

```
RAG-demo/
├── Dockerfile               # Dockerfile for building the backend service
├── docker-compose.yml       # Docker Compose file for running the backend and ChromaDB
├── rag/
│   ├── server.py            # Python HTTP server
│   ├── main.py              # Backend logic for database initialization and querying
│   ├── index.html           # Frontend HTML file
│   ├── RPA-ProDev-ModuleDEscriptions.csv  # CSV file with module descriptions
```

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- Python 3.12+ (if running locally without Docker).

## Setup and Usage

### Using Docker Compose

1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. Access the frontend:
   - Open your browser and navigate to `http://localhost:8080`.

3. Query the system:
   - Enter a question in the text box and click "Send."
   - View the results as a list and click on an item to see its description.

### Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python rag/server.py
   ```

3. Access the frontend:
   - Open your browser and navigate to `http://localhost:8080`.

## Endpoints

### `GET /index.html`
Serves the frontend HTML file.

### `POST /question`
Processes a natural language query and returns a JSON response with relevant results.

#### Request Body:
```json
{
  "question": "Your question here"
}
```

#### Response:
```json
{
  "message": "Query successful",
  "results": [
    {
      "id": "1",
      "metadata": {"name": "Module 1"},
      "document": "Description of Module 1",
      "distance": 0.123
    },
    ...
  ]
}
```

## Technologies Used

- **Backend**:
  - Python 3.12
  - ChromaDB for embedding-based retrieval
  - SQLite for structured data storage

- **Frontend**:
  - HTML and JavaScript for a simple user interface

- **Containerization**:
  - Docker and Docker Compose for easy deployment

## How It Works

1. **Database Initialization**:
   - The `main.py` script initializes a SQLite database and a ChromaDB collection.
   - Data from the `RPA-ProDev-ModuleDEscriptions.csv` file is added to both.

2. **Query Processing**:
   - The `/question` endpoint embeds the user's query and retrieves the top `k` results from ChromaDB.
   - Results include metadata, document content, and similarity scores.

3. **Frontend Interaction**:
   - Users submit a question via the HTML interface.
   - Results are displayed as a list, and clicking on an item shows its description in a popup.

## Example

1. Enter a question like:
   ```
   What is the purpose of Module 1?
   ```

2. View the results:
   - A list of relevant modules with their IDs, similarity scores, and names.

3. Click on a result to see its description in a popup.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- The sampple module descriptions are for the RPA Professional Developer training from http://learn.tungstenautomation.com
- [ChromaDB](https://www.trychroma.com/) for embedding-based retrieval.
- Python's `http.server` module for the minimalist HTTP server.
```
