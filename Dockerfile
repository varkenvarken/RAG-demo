# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the default command to run the main.py script with arguments
CMD ["python", "rag/server.py"]