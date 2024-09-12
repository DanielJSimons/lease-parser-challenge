from flask import Flask, request, jsonify
import logging
from config import OUTPUT_JSON_PATH, OUTPUT_CSV_PATH, LOG_FILE
from processing.data_loader import extract_entries
from processing.data_processing import process_data
from save_to_file import save_data
from validation.validate_output import validate_data

# Set up basic logging configuration using paths from config.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to the file specified in config.py
        logging.StreamHandler()         # Also log to the console
    ]
)

# Create the Flask app
app = Flask(__name__)

# Use the configured logger in Flask
app.logger.handlers = logging.getLogger().handlers
app.logger.setLevel(logging.INFO)

@app.route('/process', methods=['POST'])
def process_payload():
    """
    Endpoint to process the lease data payload.
    Accepts JSON payload via POST request and processes it.
    """
    try:
        data = request.json

        if not data:
            app.logger.error("No data provided in the request.")
            return jsonify({"error": "No data provided"}), 400

        entries = extract_entries(data)
        if entries is None:
            app.logger.error("Failed to extract entries from the payload.")
            return jsonify({"error": "Failed to extract entries from the payload"}), 400

        structured_lease_data = process_data(data)

        valid_data = validate_data(structured_lease_data)

        save_data(valid_data, OUTPUT_CSV_PATH, OUTPUT_JSON_PATH)

        app.logger.info(f"Data has been processed and saved to: {OUTPUT_JSON_PATH}")
        app.logger.info(f"Data has been processed and saved to: {OUTPUT_CSV_PATH}")

        return jsonify(valid_data), 200

    except Exception as e:
        app.logger.error(f"Error processing payload: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
