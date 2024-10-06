# Import dependencies
import requests
from requests.auth import HTTPBasicAuth
from config import API_KEY, SECRET_KEY


# Token URL
token_url = "https://api.schwabapi.com/v1/oauth/token"

def get_access_token():
    """
    Function to request an OAuth access token from Schwab API.
    Returns:
        access_token (str): The OAuth token required for making API requests.
    """
    payload = {
        'grant_type': 'client_credentials'
    }

    # Request access token
    token_response = requests.post(token_url, data=payload, auth=HTTPBasicAuth(API_KEY, SECRET_KEY))

    # Check if token request was successful
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data['access_token']
        return access_token
    else:
        raise Exception(f"Failed to get access token: {token_response.status_code} {token_response.text}")


