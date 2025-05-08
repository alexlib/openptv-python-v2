"""
Script to run the OpenPTV GUI.
"""

import sys

def main():
    """Main function."""
    try:
        from openptv.gui import pyptv_gui
        pyptv_gui.main()
        return 0
    except Exception as e:
        print(f"Failed to run OpenPTV GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
