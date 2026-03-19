#!/bin/bash

# Start Ollama in the background
echo "Starting Ollama server..."
ollama serve &

# Give Ollama a few seconds to initialize
sleep 5

# Start the FastAPI server on port 8080 (Cloud Run's default port)
echo "Starting FastAPI gateway..."
exec uvicorn app:app --host 0.0.0.0 --port 8080