import json
import logging


def load_json_data(input_path):
    """Load JSON data from the specified file path."""
    try:
        with open(input_path, 'r') as file:
            data = json.load(file)
        logging.info(f"Successfully loaded data from {input_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load JSON data from {input_path}: {e}")
        return None


def extract_entries(data):
    """Extract schedule entries from the loaded JSON data."""
    all_entries = []
    # Ensure the input data is a list
    if not isinstance(data, list):
        logging.error("Input data is not a list.")
        return None

    try:
        for item in data:
            # Extract each leaseschedule's scheduleEntry
            if 'leaseschedule' in item and 'scheduleEntry' in item['leaseschedule']:
                all_entries.extend(item['leaseschedule']['scheduleEntry'])
        logging.info(f"Total entries collected: {len(all_entries)}")
        return all_entries
    except (IndexError, KeyError) as e:
        logging.error(f"Error accessing JSON structure: {e}")
        return None
