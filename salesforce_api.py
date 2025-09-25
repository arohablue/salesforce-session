import requests
import os
from dotenv import load_dotenv

load_dotenv()

def authenticate_salesforce():
    url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"
    payload = {
        'grant_type': 'password',
        'client_id': os.getenv('SF_CLIENT_ID'),
        'client_secret': os.getenv('SF_CLIENT_SECRET'),
        'username': os.getenv('SF_USERNAME'),
        'password': os.getenv('SF_PASSWORD')
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def fetch_sessions(auth_data):
    headers = {
        "Authorization": f"Bearer {auth_data['access_token']}"
    }

    query = """
    SELECT Id, UsersId, SessionType, LoginType, SourceIp, ParentId, CreatedDate, LastModifiedDate 
    FROM AuthSession 
    ORDER BY LastModifiedDate DESC
    """
    url = f"{auth_data['instance_url']}/services/data/v60.0/query"
    params = {'q': query}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['records']
