def load_stylesheet(file_name="/style.qss"):

    try:
        with open(f"styles/{file_name}", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
