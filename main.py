#!/usr/bin/env python3
"""
MS Learn GUI Data Generator
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.main_window import MSLearnGUIApp

def main():
    """Main entry point for the application"""
    try:
        app = MSLearnGUIApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
