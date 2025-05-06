from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
from main import query_modules, initialize  # Import the query_modules function


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            folder_path = Path(__file__).parent
            index_path = folder_path / "index.html"
            if index_path.exists():
                # Serve the index.html file
                with open(index_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.wfile.write(b"<h1>index.html not found</h1>")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path == "/question":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                natural_query = data.get("question", "")
                if not natural_query.strip():
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Invalid question")
                    return

                # Call the query_modules function
                results = list(query_modules(natural_query, k=5))
                response = {
                    "message": "Query successful",
                    "results": [
                        {
                            "id": result.id,
                            "metadata": result.metadata,
                            "document": result.document,
                            "distance": result.distance,
                        }
                        for result in results
                    ],
                }

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    initialize()  # Initialize the database and collection
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
