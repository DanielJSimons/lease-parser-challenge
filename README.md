# Lease Parser

## Overview

Lease Parser is a tool designed to extract structured data from unstructured JSON data of lease schedules. The project
processes and validates lease entries, converting them into structured formats like CSV and JSON for easier analysis and
integration into other systems.

## Project Structure

      OrbitalWitnessTechnical
      ├── lease-parser
      │   ├── data
      │   │   ├── input
      │   │   │   └── schedule_of_notices_of_lease_examples.json
      │   │   └── output
      │   │       ├── structured_lease_data.csv
      │   │       └── structured_lease_data.json
      │   │
      │   └── logs
      │       └── application.log
      │     
      ├── src
      │   ├── api
      │   │   └── app.py
      │   ├── processing
      │   │   ├── data_loader.py
      │   │   └── data_processing.py
      │   ├── utils
      │   │   └── utils.py
      │   ├── validation
      │   │   ├── __init__.py
      │   │   └── validate_output.py
      │   ├── __init__.py
      │   ├── config.py
      │   ├── extract_info.py
      │   ├── main.py
      │   └── save_to_file.py
      ├── tests
      │   └── test_dataloader.py
      ├── README.md
      ├── requirements.txt
      └── setup.py

## Features

- **Data Extraction**: Extracts lease entries from unstructured JSON data.
- **Data Processing**: Processes data to maintain the original structure while converting it into a structured format.
- **Validation**: Validates the processed data to ensure accuracy and consistency.
- **Save Output**: Outputs the processed data into CSV and JSON formats.

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/lease-parser.git
   cd lease-parser
   ```
2. **Navitage to the Project Directory**
    ```bash
    cd OrbitalWitnessTechnical
   ```
3. **Create and Activate a Virtual Environment (Optional but advised)**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
4. **Install all dependencies**
    ```bash
    pip install -r requirements.txt
    ```
5. **My solution can be run simply through main.py**
    ```bash
    python src/main.py
   ```
6. **Alternatively the project includes a Flask-based API that allows you to process lease data by sending a JSON
   payload to the server. The API provides an endpoint to accept, process, validate, and save the structured lease data.
   This currently only saves to the output directory but could be easily implemented into a production pipeline.**

   **To start the API, run the following command in terminal from the project directory:**
   ```bash
   python src/app.py
   ```
   This will start a Flask server on [http://127.0.0.1:5000](http://127.0.0.1:5000).

   **API Endpoint**

   This endpoint processes lease data submitted as a JSON payload.

   **URL:** [http://127.0.0.1:5000/process](http://127.0.0.1:5000/process)

   **Method:** `POST`

   **Request Body:**
    - The request should include a JSON payload containing the lease data to be processed.

   **Example Request:**
   ```json
   POST /process HTTP/1.1
   Host: 127.0.0.1:5000
   Content-Type: application/json

   {
     "leaseschedule": {
       "scheduleType": "SCHEDULE OF NOTICES OF LEASE",
       "scheduleEntry": [
         {
           "entryNumber": "1",
           "entryText": [
             "28.01.2009      Transformer Chamber (Ground   23.01.2009      EGL551039  ",
             "tinted blue     Floor)                        99 years from              ",
             "(part of)                                     23.1.2009"
           ]
         }
       ]
     }
   }
   ```

   **Response:**
    - Returns a JSON response with the processed and validated data.
    - On success, the structured data is saved to the paths specified in the configuration file (`config.py`).

   **Example Response:**
   ```json
   {
     "leaseschedule": {
       "scheduleType": "SCHEDULE OF NOTICES OF LEASE",
       "scheduleEntry": [
         {
           "guid": "a1a60815-ee07-4c7b-a6d8-6ad5c1ac344c",
           "processedDateTime": "2024-09-11 19:47:27",
           "entryNumber": "1",
           "registrationDateAndPlanRef": "28.01.2009 tinted blue (part of)",
           "propertyDescription": "Transformer Chamber (Ground Floor)",
           "dateOfLeaseAndTermAsReported": "23.01.2009 99 years from 23.1.2009",
           "lesseesTitle": "EGL551039",
           "noteOne": null,
           "noteTwo": null,
           "noteThree": null,
           "noteFour": null
         }
       ]
     }
   }
   ```

7. **Possible Improvements**

   - There are many improvements to be made throughout this project if time constraints were not a factor.

       1. Complete unit testing for all methods used throughout the project. I have implemented some for the data
          loader as
          an example.
       2. Improvements to the validations given additional domain knowledge or analysis time. This would further ensure
          data integrity.
       3. Currently, all relevant information is logged to the console and saved in a dedicated .log file, in a
          production capacity this would be best stored
          in a dedicated production db.
       4. API documentation: Swagger or Postman to maintain comprehensive documentation.
       5. In a production setting the project would need containerizing with Docker.
       6. Again, in a production setting a CI/CD pipeline would need to be set up for automation of testing etc.
       7. Flask is currently only set up as a development version, disable debug mode in production.
       8. Improve API security with some form of authentication in production.
       9. Potential for monitoring the application with tools such as Grafana. This can be useful for performance,
          uptime
          or errors in an easily accessible way.
       10. Rather than removing perceived invalid rows, an additional simple field could be provided as part of the api
           response. isValid (`True, False`) or alternatively (`1, 0`). This way the user will receive the output,
           decide if they will use the data, apply additional validations or transformations.
       11. Finally, the core offering of the solution needs improving. The logic of column detection and text chunking
           needs
           improving massively.
           - Potential options are NER matching for the property descriptions.
           - Additional regex and detection for varying date formats.
           - Domain specific knowledge to understand further what is expected per column. I have identified but not
             implemented (due to time constraints) several format fixes for when items should be assigned to columns 2
             and 3 that we are currently
             misallocating to column 1.