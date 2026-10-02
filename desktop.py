"""
NETRA — AI-Powered Social Intelligence Platform (SIH26152)
Native Desktop Launcher via pywebview.

Runs Flask in a background thread and presents the platform in an isolated,
high-performance desktop window without browser chrome.
"""

import threading
import time
import webview
from app import app

HOST = "127.0.0.1"
PORT = 5000

def start_server():
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(1.2)

    webview.create_window(
        "NETRA — AI Social Intelligence Platform (SIH26152)",
        f"http://{HOST}:{PORT}",
        width=1440,
        height=900,
        min_size=(1100, 700)
    )
    webview.start()
