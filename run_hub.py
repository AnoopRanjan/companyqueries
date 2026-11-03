"""
Global IT Knowledge Hub - Top-Level Launcher
Run this script to launch the Global IT Knowledge Hub application:
    python run_hub.py
"""

import sys
import subprocess
from pathlib import Path

HUB_DIR = Path(__file__).resolve().parent / "global_it_knowledge_hub"

if __name__ == "__main__":
    print("[*] Launching Global IT Knowledge Hub from:", HUB_DIR)
    sys.exit(subprocess.call([sys.executable, str(HUB_DIR / "main.py")]))
