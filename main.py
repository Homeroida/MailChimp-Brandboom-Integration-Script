import requests
import time
import schedule
import logging
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Configuration constants
BRANDBOOM_API_KEY = '34C30B02DDD61413CD2CE0B3208C170F'
BRANDBOOM_URL = 'https://manage.brandboom.com/api/v2/customers/search'
DATE_MODIFIED = "2024-02-01"

MAILCHIMP_API_KEY = '9529dc5020ec4b3d0229f2c98023e52a-us11'
MAILCHIMP_AUDIENCE_ID = 'aa28f1bed7'
MAILCHIMP_SERVER_PREFIX = 'us11'

# Configure logging
logging.basicConfig(filename='script_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_brandboom_data():
    """
    Fetches customer data from the Brandboom API.
    """
    headers = {"accept": "application/json", "X-Api-Key": BRANDBOOM_API_KEY}
    params = {"dateModified": DATE_MODIFIED}

    response = requests.get(BRANDBOOM_URL, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for non-200 status codes
    return response.json()

def add_member_to_mailchimp(member_info):
    """
    Adds a member to the Mailchimp audience.
    """
    mailchimp = MailchimpMarketing.Client()
    mailchimp.set_config({"api_key": MAILCHIMP_API_KEY, "server": MAILCHIMP_SERVER_PREFIX})

    try:
        response = mailchimp.lists.add_list_member(MAILCHIMP_AUDIENCE_ID, member_info)
        logging.info(f"Added member with email: {member_info['email_address']}")
    except ApiClientError as error:
        logging.error(f"Email already exists in Mailchimp: {error}")

def process_customer_data(data):
    """
    Processes customer data from the Brandboom API response.
    """
    if 'value' not in data:
        logging.warning("No customer data found in the Brandboom API response.")
        return

    customers = data['value']['customers']
    for customer in customers:
        email = customer.get('email')
        if not email:
            logging.warning(f"Skipping customer entry without email: {customer}")
            continue

        member_info = prepare_member_info(customer)
        add_member_to_mailchimp(member_info)

def prepare_member_info(customer):
    """
    Prepares member info for Mailchimp from customer data.
    """
    merge_fields = {
        "FNAME": customer.get('buyerName'),
        "LNAME": "",
        "ADDRESS1": customer.get('address1'),
        "PHONE": customer.get('phone'),
        "BUYERNAME": customer.get('buyerName'),
        "CUSTOMERID": customer.get('customerID'),
        "ACCOUNTID": customer.get('accountID'),
        "CCODE1": customer.get('customerCode1'),
        "CCODE2": customer.get('customerCode2'),
        "ADDRESS2": customer.get('address2'),
        "CITY": customer.get('city'),
        "STATECODE": customer.get('stateCode'),
        "POSTALCODE": customer.get('postalCode'),
        "COUNTRY": customer.get('country'),
        "COUNTRYC": customer.get('countryCode')
    }
    
    return {
        "email_address": customer.get('email'),
        "status": "subscribed",
        "merge_fields": merge_fields
    }

def job():
    """
    Job to be scheduled.
    """
    print('start a job')
    try:
        data = get_brandboom_data()
        if data:
            process_customer_data(data)
    except requests.RequestException as e:
        logging.error(f"Error fetching data from Brandboom API: {e}")
    except ApiClientError as e:
        logging.error(f"Mailchimp API error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Run the job immediately
job()

# Schedule the job to run every 3 hours after the initial run
schedule.every(3).hours.do(job)

# Infinite loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
