import csv
import json
import logging
from typing import List, Dict, Any


def flatten_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Helper function for save_to_csv.
    Flatten the nested lease schedule data to match the expected CSV structure.

    :param data: A list of dictionaries containing the structured lease data with nested schedule entries.
    :return: A flattened list of dictionaries suitable for CSV output.
    """
    flattened_data = []

    for item in data:
        # Check if 'leaseschedule' and 'scheduleEntry' keys exist
        if 'leaseschedule' in item and 'scheduleEntry' in item['leaseschedule']:
            for entry in item['leaseschedule']['scheduleEntry']:
                # Add the flattened entry to the list
                flattened_data.append(entry)

    return flattened_data


def save_to_csv(data: List[Dict[str, Any]], csv_file_path: str) -> None:
    """
    Save the structured data to a CSV file.

    :param data: A list of dictionaries containing the structured lease data.
    :param csv_file_path: The file path where the CSV will be saved.
    """
    # Define field names based on the expected output structure - Could be made dynamic
    fieldnames = [
        "guid", "processedDateTime", "entryNumber", "registrationDateAndPlanRef",
        "propertyDescription", "dateOfLeaseAndTermAsReported", "lesseesTitle",
        "noteOne", "noteTwo", "noteThree", "noteFour"
    ]

    # Flatten the data to match the expected CSV structure
    flattened_data = flatten_data(data)

    # Write data to CSV
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_data)
        logging.info(f"Data successfully saved to {csv_file_path}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")


def save_to_json(data: List[Dict[str, Any]], json_file_path: str) -> None:
    """
    Save the structured data to a JSON file.

    :param data: A list of dictionaries containing the structured lease data.
    :param json_file_path: The file path where the JSON will be saved.
    """
    try:
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)  # Indent for prettier formatting
        logging.info(f"Data successfully saved to {json_file_path}")
    except Exception as e:
        logging.error(f"Error saving data to JSON: {e}")


def save_data(structured_lease_data: List[Dict[str, Any]], output_path_csv: str, output_path_json: str) -> None:
    """
    Save the structured data to both CSV and JSON files.

    :param structured_lease_data: A list of dictionaries containing the structured lease data.
    :param output_path_csv: The file path where the CSV will be saved.
    :param output_path_json: The file path where the JSON will be saved.
    """
    try:
        save_to_csv(structured_lease_data, output_path_csv)
        save_to_json(structured_lease_data, output_path_json)
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
