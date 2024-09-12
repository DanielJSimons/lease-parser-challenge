import json
from typing import List, Dict, Any, Optional
from unittest.mock import patch, mock_open
from processing.data_loader import load_json_data, extract_entries

def test_load_json_data_success() -> None:
    """
    Test loading JSON data successfully from a valid file.
    """
    sample_data: List[Dict[str, Any]] = [{"leaseschedule": {"scheduleType": "Test", "scheduleEntry": [{"entryNumber": "1"}]}}]
    sample_json: str = json.dumps(sample_data)

    with patch("builtins.open", mock_open(read_data=sample_json)):
        result: Optional[List[Dict[str, Any]]] = load_json_data("dummy_path.json")
        assert result == sample_data

def test_load_json_data_file_not_found() -> None:
    """
    Test loading JSON data from a file path that does not exist.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        result: Optional[List[Dict[str, Any]]] = load_json_data("non_existent_path.json")
        assert result is None

def test_load_json_data_invalid_json() -> None:
    """
    Test handling of invalid JSON content.
    """
    invalid_json: str = "{invalid: json"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        result: Optional[List[Dict[str, Any]]] = load_json_data("dummy_path.json")
        assert result is None

def test_extract_entries_success() -> None:
    """
    Test extracting entries successfully from well-structured data.
    """
    sample_data: List[Dict[str, Any]] = [
        {
            "leaseschedule": {
                "scheduleType": "Test",
                "scheduleEntry": [{"entryNumber": "1"}, {"entryNumber": "2"}]
            }
        },
        {
            "leaseschedule": {
                "scheduleType": "Test",
                "scheduleEntry": [{"entryNumber": "3"}]
            }
        }
    ]

    result: List[Dict[str, Any]] = extract_entries(sample_data)
    assert len(result) == 3
    assert result == [{"entryNumber": "1"}, {"entryNumber": "2"}, {"entryNumber": "3"}]

def test_extract_entries_missing_keys() -> None:
    """
    Test handling of missing keys in the data structure.
    """
    sample_data: List[Dict[str, Any]] = [{"wrongKey": "value"}]

    result: List[Dict[str, Any]] = extract_entries(sample_data)
    assert result == []

def test_extract_entries_malformed_data() -> None:
    """
    Test handling of malformed data (non-list input).
    """
    malformed_data: Dict[str, Any] = {"leaseschedule": {"scheduleType": "Test", "scheduleEntry": [{"entryNumber": "1"}]}}

    result: Optional[List[Dict[str, Any]]] = extract_entries(malformed_data)
    assert result is None
