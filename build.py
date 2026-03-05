import subprocess
import sys

import config
from generate_licenses import generate_licenses_file


def build_app():
    print("Step 1: Updating third-party licenses...")
    generate_licenses_file()

    print("\nStep 2: Building with PyInstaller...")
    # Adjust this list with your actual PyInstaller flags and main script name
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--noconsole",
        "--onefile",
        "--add-data", "licenses:licenses",
        "--add-data", "styles:styles",
        "--add-data", "assets:assets",
        "--icon", "assets/app_icon.ico",
        "--name", config.APP_NAME,
        "main.py"
    ]

    subprocess.run(pyinstaller_cmd, check=True)
    print("\nBuild complete!")


if __name__ == "__main__":
    build_app()
