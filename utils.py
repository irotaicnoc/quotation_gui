import os
import sys

import config


def load_stylesheet(file_name="style.qss"):

    # Check if running as a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    # Build the correct absolute path
    file_path = os.path.join(base_path, config.style_folder_path, file_name)

    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
