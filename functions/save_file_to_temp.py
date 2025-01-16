import tempfile
import os

def save_file_to_temp(file):
    """
    Save a file-like object to a temporary location and return the path.

    Args:
        file: A file-like object containing the uploaded data.

    Returns:
        str: The path to the temporary file.
    """
    # Save the file to a temporary location
    file.seek(0)  # Ensure the file pointer is at the start
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
    return temp_file_path
