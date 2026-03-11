#!/bin/bash
# Start the Streamlit frontend application
# Render/Heroku dynamically injects the $PORT environment variable
echo "Starting Streamlit Application..."
streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0
