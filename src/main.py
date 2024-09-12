import logging

from config import INPUT_JSON_PATH, OUTPUT_CSV_PATH, OUTPUT_JSON_PATH
from processing.data_loader import load_json_data, extract_entries
from processing.data_processing import process_data
from save_to_file import save_data
from validation.validate_output import validate_data

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    data = load_json_data(INPUT_JSON_PATH)

    if data is None:
        logging.error("Failed to load data. Exiting.")
        return

    # Extract entries
    entries = extract_entries(data)

    if entries is None:
        logging.error("Failed to extract entries. Exiting.")
        return

    # Process data to maintain original structure
    structured_data = process_data(data)

    # Validate data
    valid_data = validate_data(structured_data)

    save_data(valid_data, OUTPUT_CSV_PATH, OUTPUT_JSON_PATH)

    logging.info(f"Data has been processed and saved to: {OUTPUT_JSON_PATH}")
    logging.info(f"Data has been processed and saved to: {OUTPUT_CSV_PATH}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
