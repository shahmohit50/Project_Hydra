#!/bin/bash
set -e

echo "🐉 Hydra Awakening Sequence Starting..."

# Start Ollama server in background
echo "📦 Starting Ollama service..." 
ollama serve &
OLLAMA_PID=$!
# ollama server --port 11434 &
# OLLAMA_PID=$!

# Wait a few seconds for Ollama to start
sleep 5

# Pull mistral model (if not already cached in Docker layer/volume) 
echo "⬇️ Pulling mistral model (this may take a while the first time)..." 
ollama pull mistral:7b-instruct-v0.2-q4_K_M || { echo "❌ Failed to pull mistral"; kill $OLLAMA_PID; exit 1; }

# Start Hydra orchestrator
python core/orchestrator.py

# Stop Ollama when Hydra exits
kill $OLLAMA_PID
