import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, '..', 'lease-parser', 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# File paths
INPUT_JSON_PATH = os.path.join(INPUT_DIR, 'schedule_of_notices_of_lease_examples.json')
OUTPUT_CSV_PATH = os.path.join(OUTPUT_DIR, 'structured_lease_data.csv')
OUTPUT_JSON_PATH = os.path.join(OUTPUT_DIR, 'structured_lease_data.json')

# Log directory and file
LOG_DIR = os.path.join(BASE_DIR, '..', 'lease-parser', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'application.log')

# Ensure required directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)