import logging
import re
from typing import List, Dict, Optional, Tuple


def initialize_empty_columns_and_notes() -> Tuple[Dict[str, List[str]], Dict[str, Optional[str]]]:
    """
    Initialize dictionaries for columns and notes with empty values.
    """
    columns = {
        'registrationDateAndPlanRef': [],
        'propertyDescription': [],
        'dateOfLeaseAndTermAsReported': [],
        'lesseesTitle': []
    }
    notes = {'noteOne': None, 'noteTwo': None, 'noteThree': None,
             'noteFour': None}  # Could be dynamically created although in the examples there are no more than four.
    return columns, notes


def separate_main_text_and_notes(entry_text: List[str]) -> Tuple[List[str], List[str]]:
    """
    Split entry text lines into main text lines and note lines based on the presence of 'NOTE'.
    """
    note_pattern = re.compile(r'^NOTE\s*(\d*)\:?', re.IGNORECASE)
    note_lines = []  # List to collect note lines
    main_text = []  # List to collect main text lines

    i = 0
    while i < len(entry_text):
        line = entry_text[i].strip() if entry_text[i] else ''
        if note_pattern.match(line):
            note_text = line  # Start collecting a note line
            i += 1
            # Collect subsequent lines that are part of the note
            while i < len(entry_text) and not note_pattern.match(entry_text[i].strip()):
                note_text += ' ' + entry_text[i].strip()
                i += 1
            note_lines.append(note_text)  # Add collected note to the list
        else:
            main_text.append(line)  # Add line to main text
            i += 1
    return main_text, note_lines


def parse_main_text_into_columns(main_text: List[str], columns: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Process the main text lines and fill the columns dictionary accordingly.
    """
    first_line_length = 73  # Expected length of the first line, this seems consistent across all entries. Not strictly needed.
    date_pattern = re.compile(
        r'^\d{1,2}\.\d{1,2}\.\d{4}$')  # Rigid pattern to identify dates. Can be improved for all date formats.
    subsequent_to_part_of = False  # Flag to handle lines following '(part of)' as this is a common data entry.

    for i, line in enumerate(main_text):
        line = line.strip()

        if i == 0 and len(line) >= first_line_length:
            extract_columns_from_first_line(line, columns)  # Process the first line separately
        elif "(part of)" in main_text[i - 1] if i > 0 else False:  # Typical string to use as anchor
            subsequent_to_part_of = True
        elif date_pattern.match(line):
            columns['dateOfLeaseAndTermAsReported'].append(line)
        elif subsequent_to_part_of and len(re.split(r'\s+', line)) == 1:
            columns['dateOfLeaseAndTermAsReported'].append(line)
        else:
            subsequent_to_part_of = False
            extract_columns_from_other_lines(line, columns)
    return columns


def extract_columns_from_first_line(line: str, columns: Dict[str, List[str]]) -> None:
    """
    Split the first line into respective columns based on spaces.
    """
    parts = re.split(r'\s{3,}', line.strip())  # Split by at least three spaces
    if len(parts) > 0:
        columns['registrationDateAndPlanRef'].append(parts[0].strip())
    if len(parts) > 1:
        columns['propertyDescription'].append(parts[1].strip())
    if len(parts) > 2:
        columns['dateOfLeaseAndTermAsReported'].append(parts[2].strip())
    if len(parts) > 3:
        columns['lesseesTitle'].append(parts[3].strip())


def extract_columns_from_other_lines(line: str, columns: Dict[str, List[str]]) -> None:
    """
    Split other lines into columns based on space patterns.
    """
    parts = re.split(r'\s{2,}', line.strip())  # Split by at least two spaces
    if len(parts) == 1:
        columns['registrationDateAndPlanRef'].append(parts[0].strip())
        columns['propertyDescription'].append('')
        columns['dateOfLeaseAndTermAsReported'].append('')
        columns['lesseesTitle'].append('')
    elif len(parts) == 2:
        columns['registrationDateAndPlanRef'].append(parts[0].strip())
        columns['propertyDescription'].append('')
        columns['dateOfLeaseAndTermAsReported'].append(parts[1].strip())
        columns['lesseesTitle'].append('')
    elif len(parts) == 3:
        columns['registrationDateAndPlanRef'].append(parts[0].strip())
        columns['propertyDescription'].append(parts[1].strip())
        columns['dateOfLeaseAndTermAsReported'].append(parts[2].strip())
        columns['lesseesTitle'].append('')
    elif len(parts) > 3:
        columns['registrationDateAndPlanRef'].append(parts[0].strip())
        columns['propertyDescription'].append(parts[1].strip())
        columns['dateOfLeaseAndTermAsReported'].append(parts[2].strip())
        columns['lesseesTitle'].append(parts[3].strip())


def parse_notes_into_dictionary(note_lines: List[str], notes: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """
    Process note lines and fill the notes dictionary with values.
    """
    for idx, note in enumerate(note_lines, start=1):
        if idx > 4:
            break  # Limit to a maximum of 4 notes
        note_key = f'note{["One", "Two", "Three", "Four"][idx - 1]}'
        notes[note_key] = note.strip()
    return notes


def construct_result(columns: Dict[str, List[str]], notes: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """
    Construct the final result dictionary combining columns and notes.
    """
    return {
        "registrationDateAndPlanRef": ' '.join(columns['registrationDateAndPlanRef']).strip() or None,
        "propertyDescription": ' '.join(columns['propertyDescription']).strip() or None,
        "dateOfLeaseAndTermAsReported": ' '.join(columns['dateOfLeaseAndTermAsReported']).strip() or None,
        "lesseesTitle": ' '.join(columns['lesseesTitle']).strip() or None,
        "noteOne": notes.get('noteOne').strip() if notes.get('noteOne') else None,
        "noteTwo": notes.get('noteTwo').strip() if notes.get('noteTwo') else None,
        "noteThree": notes.get('noteThree').strip() if notes.get('noteThree') else None,
        "noteFour": notes.get('noteFour').strip() if notes.get('noteFour') else None,
    }


def parse_entry_text_into_structured_data(entry_text: Optional[List[str]]) -> Dict[str, Optional[str]]:
    """
    Main function to parse entry text into structured columns and notes.

    :param entry_text: List of entry text lines.
    :return: A dictionary containing structured columns and notes.
    """
    if entry_text is None:
        logging.warning("entryText is None, skipping this entry.")
        columns, notes = initialize_empty_columns_and_notes()
        return construct_result(columns, notes)

    columns, notes = initialize_empty_columns_and_notes()
    main_text, note_lines = separate_main_text_and_notes(entry_text)
    columns = parse_main_text_into_columns(main_text, columns)
    notes = parse_notes_into_dictionary(note_lines, notes)
    return construct_result(columns, notes)
