import os
from functions.save_file_to_temp import save_file_to_temp
from flask import request, jsonify

def generic_audio_endpoint(process_function, response_key):
    """
    Generic audio endpoint handler to process a file with the specified function.

    :param process_function: Function to process the audio file.
    :param response_key: Key for the response JSON.
    :return: JSON response with processed results.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        temp_file_path = save_file_to_temp(file)
        try:
            # Call the provided processing function with the temporary file path
            results = process_function(temp_file_path)
        finally:
            os.remove(temp_file_path)  # Ensure the temporary file is always cleaned up

        # Wrap the results in the specified response key
        response = {response_key: results}
        return jsonify(response), 200
    except Exception as e:
        # Return a standardized error response
        return jsonify({"error": str(e)}), 500