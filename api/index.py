import sys
import os

# Add root directory to sys.path so app and engine are importable
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

# Standard entrypoints for Vercel Serverless Functions
application = app
handler = app
