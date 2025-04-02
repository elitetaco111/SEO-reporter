import os
import json
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Authenticate and create the service object
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
CLIENT_SECRETS_FILE = 'client_secret_473146300778-k68g02h1iqftcukodvm29j5clsn3num2.apps.googleusercontent.com.json'

def authenticate_oauth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_indexed_pages(service, site_url):
    # Get a list of indexed pages
    request = service.urlInspection().index().list(siteUrl=site_url)
    response = request.execute()

    # Process and save the data
    return response

if __name__ == '__main__':
    site_url = 'https://www.rallyhouse.com'  # Replace with your site URL
    credentials = authenticate_oauth()
    service = build('searchconsole', 'v1', credentials=credentials)
    indexed_pages = get_indexed_pages(service, site_url)

    # Save data to CSV or JSON
    with open('indexed_pages.json', 'w') as f:
        json.dump(indexed_pages, f)
