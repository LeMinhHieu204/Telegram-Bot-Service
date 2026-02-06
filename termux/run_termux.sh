#!/data/data/com.termux/files/usr/bin/bash
set -e
python -m venv .venv
. .venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
python -m app.main
