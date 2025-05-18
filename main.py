"""
Name: Christopher Sharp
Course: CS499 Computer Science Capstone
Date Last Modified: 05-18-2025

Description:
    main.py
    Runs the main application
"""

from __future__ import annotations
import logging
import sys
from gui.app import AnimalApp

# Configuring logger to display
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logging.info("Starting")

if __name__ == '__main__':
    app = AnimalApp()
    app.mainloop()
