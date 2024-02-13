import requests
import json
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Brandboom API configuration
BRANDBOOM_API_KEY = '34C30B02DDD61413CD2CE0B3208C170F'
BRANDBOOM_URL = 'https://manage.brandboom.com/api/v2/customers/search'
DATE_MODIFIED = "2024-02-01"

# Mailchimp configuration
YOUR_API_KEY = '76106b99b98a4631ddc7cb848ffb9fa3-us11'
MAILCHIMP_AUDIENCE_ID = 'aa28f1bed7'
YOUR_SERVER_PREFIX = 'us11'

# Initialize Mailchimp client
mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
    "api_key": YOUR_API_KEY,
    "server": YOUR_SERVER_PREFIX
})

def get_brandboom_data():
    """
    Sends a GET request to the Brandboom API and returns the JSON response.
    """
    brandboom_headers = {
        "accept": "application/json",
        "X-Api-Key": BRANDBOOM_API_KEY,
    }

    brandboom_params = {
        "dateModified": DATE_MODIFIED
    }

    response = requests.get(BRANDBOOM_URL, headers=brandboom_headers, params=brandboom_params)
    return response.json() if response.status_code == 200 else None

def add_member_to_mailchimp(member_info):
    """
    Adds a member to the Mailchimp audience.
    """
    try:
        response = mailchimp.lists.add_list_member(MAILCHIMP_AUDIENCE_ID, member_info)
        print("Added member with email:", member_info['email_address'])
    except ApiClientError as error:
        print("An exception occurred while adding member to Mailchimp:", error)

def process_customer_data(data):
    """
    Processes customer data from Brandboom API response.
    """
    if 'value' in data:
        customers = data['value']['customers']
        for customer in customers:
            if 'email' not in customer or not customer['email']:
                print("Skipping customer entry without email:", customer)
                continue
            member_info = prepare_member_info(customer)
            add_member_to_mailchimp(member_info)
    else:
        print("No customer data found in the Brandboom API response.")

def prepare_member_info(customer):
    """
    Prepares member info for Mailchimp from customer data.
    """
    return {
        "email_address": customer.get('email'),
        "status": "subscribed",
        "merge_fields": {
            "FNAME": customer.get('buyerName'),
            "LNAME": "",  # You can add last name if available
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
            "COUNTRYCOD": customer.get('countryCode')
        }
    }

def main():
    """
    Main function to orchestrate the process.
    """
    try:
        data = get_brandboom_data()
        if data:
            process_customer_data(data)
        else:
            print("Failed to retrieve customer data from the Brandboom API.")
    except Exception as e:
        print("An exception occurred:", str(e))

if __name__ == "__main__":
    main()
