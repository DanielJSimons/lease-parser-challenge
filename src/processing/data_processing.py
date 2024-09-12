import logging
from typing import List, Dict, Any

from extract_info import parse_entry_text_into_structured_data
from utils.utils import generate_guid, update_date_time


def process_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process each entry by extracting its text, splitting it into columns, and
    adding unique identifiers and timestamps.

    :param entries: A list of dictionaries containing the raw entry data.
    :return: A list of dictionaries with processed entry data, including GUIDs and timestamps.
    """
    results = []

    for entry in entries:
        # Extract entry text; default to an empty list if not present
        entry_text = entry.get('entryText', [])

        # Split entry text into structured columns (e.g., registration date, property description, etc..)
        split_result = parse_entry_text_into_structured_data(entry_text)

        # Append processed data with a unique GUID and timestamp for traceability since there are so many entries
        results.append({
            "guid": generate_guid(),
            "processedDateTime": update_date_time(),
            "entryNumber": entry.get('entryNumber', None),
            **split_result  # Unpack split column data into the dictionary
        })

    return results


def process_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process the entire data structure by retaining the original JSON hierarchy while processing
    each entry's details.

    :param data: A list of dictionaries representing the full input data structure.
    :return: A list of dictionaries with the processed data, maintaining the original hierarchy.
    """
    processed_data = []

    for item in data:
        if 'leaseschedule' in item and 'scheduleEntry' in item['leaseschedule']:
            # Process entries within each leaseschedule
            processed_entries = process_entries(item['leaseschedule']['scheduleEntry'])

            # Reconstruct the leaseschedule with processed entries to retain the structure
            processed_schedule = {
                "leaseschedule": {
                    "scheduleType": item['leaseschedule'].get('scheduleType', 'Unknown Schedule Type'),
                    "scheduleEntry": processed_entries
                }
            }

            # Append the processed schedule to the final data
            processed_data.append(processed_schedule)

    logging.info("Processing completed, retaining original data structure.")
    return processed_data
