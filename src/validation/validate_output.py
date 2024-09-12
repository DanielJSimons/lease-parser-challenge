import logging
import re
from typing import List, Dict, Any, Optional


def validate_data(structured_lease_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validate each entry within the structured lease data and filter out only the valid entries.

    :param structured_lease_data: A list of dictionaries containing the structured lease data with nested scheduleEntries.
    :return: A list of dictionaries containing only the valid structured lease entries.
    """
    logging.info("Validating data...")
    valid_data = []

    for idx, item in enumerate(structured_lease_data):
        # Check if the required keys exist
        if 'leaseschedule' in item and 'scheduleEntry' in item['leaseschedule']:
            for entry_idx, entry in enumerate(item['leaseschedule']['scheduleEntry']):
                # Validate each row and append valid ones
                if validate_row(entry, entry_idx):
                    valid_data.append(entry)

    logging.info(
        f"Total valid entries: {len(valid_data)} / {sum(len(item['leaseschedule']['scheduleEntry']) for item in structured_lease_data if 'leaseschedule' in item and 'scheduleEntry' in item['leaseschedule'])}")
    return valid_data


def validate_row(row: Dict[str, Any], idx: int) -> bool:
    """
    Validate all columns of a single row and return True if valid, False otherwise.

    :param row: A dictionary containing a single row of structured lease data.
    :param idx: The index of the row being validated.
    :return: True if the row is valid, False otherwise.
    """
    guid = row.get("guid", "Unknown GUID")

    # Validate each column using specific functions, returning False on any failure
    return all([
        validate_guid(row.get("guid"), idx, guid),
        validate_processed_datetime(row.get("processedDateTime"), idx, guid),
        validate_entry_number(row.get("entryNumber"), idx, guid),
        validate_registration_date_and_plan_ref(row.get("registrationDateAndPlanRef"), idx, guid),
        validate_property_description(row.get("propertyDescription"), idx, guid),
        validate_date_of_lease_and_term(row.get("dateOfLeaseAndTerm"), idx, guid),
        validate_lessees_title(row.get("lesseesTitle"), idx, guid),
        validate_notes(row.get("noteOne"), "noteOne", idx, guid),
        validate_notes(row.get("noteTwo"), "noteTwo", idx, guid),
        validate_notes(row.get("noteThree"), "noteThree", idx, guid),
        validate_notes(row.get("noteFour"), "noteFour", idx, guid),
    ])


def validate_guid(value: Optional[Any], idx: int, guid: str) -> bool:
    if not isinstance(value, str):
        log_error("guid", value, idx, guid)
        return False
    return True


def validate_processed_datetime(value: Optional[Any], idx: int, guid: str) -> bool:
    if not isinstance(value, str):
        log_error("processedDateTime", value, idx, guid)
        return False
    return True


def validate_entry_number(value: Optional[Any], idx: int, guid: str) -> bool:
    if not isinstance(value, int):
        if isinstance(value, str) and value.isdigit():
            return True  # Consider as valid if conversion is possible
        log_error("entryNumber", value, idx, guid)
        return False
    return True


def validate_registration_date_and_plan_ref(value: Optional[Any], idx: int, guid: str) -> bool:
    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b')
    if not isinstance(value, (str, type(None))) or (isinstance(value, str) and not date_pattern.search(value)):
        log_error("registrationDateAndPlanRef", value, idx, guid, "Does not contain a valid date")
        return False
    return True


def validate_property_description(value: Optional[Any], idx: int, guid: str) -> bool:
    if not isinstance(value, (str, type(None))):
        log_error("propertyDescription", value, idx, guid)
        return False
    return True


def validate_date_of_lease_and_term(value: Optional[Any], idx: int, guid: str) -> bool:
    if not isinstance(value, (str, type(None))):
        log_error("dateOfLeaseAndTerm", value, idx, guid)
        return False
    if value is not None:
        date_pattern = re.compile(r'\d{1,2}\.\d{1,2}\.\d{4}')
        matches = date_pattern.findall(value)
        if len(matches) < 2:
            log_error("dateOfLeaseAndTerm", value, idx, guid, "Does not contain two or more dates")
            return False
    return True


def validate_lessees_title(value: Optional[Any], idx: int, guid: str) -> bool:
    lessees_title_pattern = re.compile(r'^[A-Z]{1,3}\d{4,6}$', re.IGNORECASE)
    if not isinstance(value, (str, type(None))):
        log_error("lesseesTitle", value, idx, guid)
        return False
    elif value is not None and not lessees_title_pattern.match(value.upper()):
        log_error("lesseesTitle", value, idx, guid, "Pattern Mismatch")
        return False
    return True


def validate_notes(value: Optional[Any], column: str, idx: int, guid: str) -> bool:
    if not isinstance(value, (str, type(None))):
        log_error(column, value, idx, guid)
        return False
    return True


def log_error(column: str, value: Any, idx: int, guid: str, issue: Optional[str] = None) -> None:
    issue_description = issue if issue else type(value).__name__
    logging.error(
        f"Data Type Error in Column: {column} | GUID: {guid} | Row: {idx} | Value: {value} | Issue: {issue_description}")
