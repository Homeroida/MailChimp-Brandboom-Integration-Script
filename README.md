# Brandboom Customer Data Integration with Mailchimp

This project aims to integrate customer data obtained from the Brandboom API with a Mailchimp audience. It fetches customer data from the Brandboom API and adds the obtained information to a specified Mailchimp audience. The integration is scheduled to run periodically using the Schedule library.

## Project Structure

- **script.py**: Contains the main Python script for data integration.
- **README.md**: This file, providing an overview of the project.
- **script_logs.log**: Log file to capture script execution logs.

## Installation

1. Clone the repository to your local machine:

```bash
git clone <repository_url>
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the script, make sure to configure the following constants in `script.py`:

- `BRANDBOOM_API_KEY`: Your Brandboom API key.
- `BRANDBOOM_URL`: Brandboom API endpoint for customer data.
- `DATE_MODIFIED`: Date modified parameter for Brandboom API request.
- `MAILCHIMP_API_KEY`: Your Mailchimp API key.
- `MAILCHIMP_AUDIENCE_ID`: ID of the Mailchimp audience to which members will be added.
- `MAILCHIMP_SERVER_PREFIX`: Mailchimp server prefix (e.g., 'us11').

## Usage

To run the integration script:

```bash
python script.py
```

The script will fetch customer data from Brandboom, process it, and add members to the specified Mailchimp audience.

## Scheduling

The integration script is scheduled to run periodically using the Schedule library. By default, it runs every minute. You can adjust the scheduling frequency by modifying the `schedule.every()` line in the script.

## Logging

Execution logs are captured in the `script_logs.log` file. You can review these logs for insights into script execution and any encountered errors.

## Error Handling

The script incorporates error handling for various scenarios, including API request errors and unexpected exceptions. Error messages are logged for debugging purposes.

## Dependencies

- `requests`: For making HTTP requests to the Brandboom API.
- `schedule`: For scheduling periodic script execution.
- `logging`: For capturing script execution logs.
- `mailchimp_marketing`: Official Mailchimp Marketing API client for Python.


