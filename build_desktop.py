"""
NETRA Desktop Installer Builder
================================
Run this script once to create a standalone Windows .exe
Usage:  python build_desktop.py
Output: netra_desktop_dist/NETRA.exe
"""

import subprocess
import sys
import os

# ── Step 1: Install PyInstaller if missing ──────────────────
print("[NETRA BUILD] Checking PyInstaller...")
try:
    import PyInstaller
    print(f"  PyInstaller {PyInstaller.__version__} found.")
except ImportError:
    print("  Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# ── Step 2: Build command ───────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--onefile",                          # single .exe
    "--windowed",                          # no console window
    "--name", "NETRA",
    "--icon", os.path.join(ROOT, "static", "img", "netra_logo.png"),
    "--add-data", f"{os.path.join(ROOT, 'templates')}{os.pathsep}templates",
    "--add-data", f"{os.path.join(ROOT, 'static')}{os.pathsep}static",
    "--add-data", f"{os.path.join(ROOT, 'data')}{os.pathsep}data",
    "--add-data", f"{os.path.join(ROOT, 'engine')}{os.pathsep}engine",
    "--distpath", os.path.join(ROOT, "netra_desktop_dist"),
    "--workpath", os.path.join(ROOT, "netra_build_temp"),
    "--specpath", ROOT,
    "--hidden-import", "flask",
    "--hidden-import", "networkx",
    "--hidden-import", "numpy",
    "--hidden-import", "webview",
    "--hidden-import", "engineio.async_drivers.threading",
    os.path.join(ROOT, "desktop.py"),
]

print("\n[NETRA BUILD] Building NETRA.exe — this will take 2-4 minutes...\n")
result = subprocess.run(cmd, cwd=ROOT)

if result.returncode == 0:
    exe_path = os.path.join(ROOT, "netra_desktop_dist", "NETRA.exe")
    print("\n" + "=" * 60)
    print("  ✅  BUILD SUCCESSFUL!")
    print(f"  📦  Installer: {exe_path}")
    print("=" * 60)
    print("\n  Give judges the 'netra_desktop_dist' folder.")
    print("  They just double-click NETRA.exe — no Python needed!\n")
else:
    print("\n❌ Build failed. See errors above.")
    sys.exit(1)
