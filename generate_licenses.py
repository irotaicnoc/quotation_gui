import subprocess

import config


def generate_licenses_file():
    output_path = config.LICENSES_FOLDER_PATH / config.THIRD_PARTY_LICENSE_FILE_NAME
    output_path.parent.mkdir(exist_ok=True)  # Ensure the licenses folder exists

    try:
        # Run the command and capture the output as a UTF-8 string
        result = subprocess.run(
            ["pip-licenses", "--with-license-file", "--format=json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )

        # Write the clean JSON string directly to the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"Successfully updated {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to generate licenses. Ensure pip-licenses is installed.\n{e}")


if __name__ == "__main__":
    generate_licenses_file()
