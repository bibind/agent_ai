#!/bin/bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi
echo "Environment ready. Activate with 'source .venv/bin/activate'"
