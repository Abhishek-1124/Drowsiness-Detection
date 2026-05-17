#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
  echo "Error: .venv not found. Run ./setup_venv.sh first."
  exit 1
fi

source .venv/bin/activate
streamlit run app.py --server.port 8501
