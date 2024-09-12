import uuid
from datetime import datetime


def generate_guid():
    """Generate a unique identifier for each row."""
    return str(uuid.uuid4())


def update_date_time():
    """Generate a datetime for each row."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
