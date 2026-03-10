#!/bin/bash
# Start the FastAPI webhook server in the background on port 8000
echo "Starting FastAPI Webhook Server..."
uvicorn webhook:app --host 0.0.0.0 --port 8000 &

# Start the Streamlit frontend application
# Render/Heroku dynamically injects the $PORT environment variable
echo "Starting Streamlit Application..."
streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0
