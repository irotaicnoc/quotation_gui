import os
import sys

import config


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_stylesheet(file_name="style.qss"):
    file_path = resource_path(os.path.join(config.STYLES_FOLDER_PATH, file_name))
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
