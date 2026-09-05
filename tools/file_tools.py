from pathlib import Path


def search_and_read_file(base_dir: str, file_name: str) -> str:
    """Recursively search for a file within a base directory and return its contents."""
    try:
        base_path = Path(base_dir).resolve()
        if not base_path.exists() or not base_path.is_dir():
            return f"Error: Base directory '{base_dir}' does not exist or is not a directory."

        # Recursively search for the file
        matches = list(base_path.rglob(file_name))

        if not matches:
            return f"Error: File '{file_name}' not found within '{base_dir}'."

        # Take the first match found
        file_path = matches[0]

        # Read the file contents safely
        content = file_path.read_text(encoding="utf-8")
        return content

    except PermissionError:
        return f"Error: Permission denied when trying to access '{file_name}'."
    except Exception as e:
        return f"Error reading file: {str(e)}"
