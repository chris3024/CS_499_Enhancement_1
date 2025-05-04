"""
main.py
Runs the main application
"""
from __future__ import annotations
import logging, sys

# Configuring logger to display
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logging.info("Starting")

from gui.app import AnimalApp

if __name__ == '__main__':
    app = AnimalApp()
    app.mainloop()
