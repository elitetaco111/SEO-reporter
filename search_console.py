import datetime
import logging
import os
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up OAuth2 credentials
CLIENT_SECRETS_FILE = "client_secret_473146300778-k68g02h1iqftcukodvm29j5clsn3num2.apps.googleusercontent.com.json" 
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

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

# Build the Search Console API service
def get_search_console_service():
    creds = authenticate_oauth()
    service = build('searchconsole', 'v1', credentials=creds)
    return service

SITE_URL = "https://www.rallyhouse.com" 

#set date filters
date1 = datetime.date.today()
timedelta = datetime.timedelta(days=1)
date2 = date1 - timedelta #yesterday (cannot generate the report for today)
timedelta = datetime.timedelta(days=9)
date3 = date1 - timedelta #9 days ago to generate consistent sun-mon reports
START_DATE = date3.strftime("%Y-%m-%d") #start date
END_DATE = date2.strftime("%Y-%m-%d") #end date

#build search console API request
request = {
    "startDate": START_DATE,  #start date
    "endDate": END_DATE,    #end date
    "dimensions": ["Query"],  #Filter Request
    "rowLimit": 10000,  #Max rows per request
    "orderBy":[
    {
      "field": "impressions",
      "order": "descending"
    }]
}

#authenticates and fetches data from Search Console API as well as saves it to a CSV file
def fetch_search_console_datav1(site_url, flag):
    service = get_search_console_service()
    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()

    #convert API response to Pandas datafrane
    if flag:
        if "rows" in response:
            data = []
            for row in response["rows"]:
                entry = {
                    "Query": row["keys"][0] if len(row["keys"]) > 0 else None,
                    "Page": row["keys"][1] if len(row["keys"]) > 1 else None,
                    "Device": row["keys"][2] if len(row["keys"]) > 2 else None,
                    "Country": row["keys"][3] if len(row["keys"]) > 3 else None,
                    "Clicks": row.get("clicks", 0),
                    "Impressions": row.get("impressions", 0),
                    "CTR": row.get("ctr", 0),
                    "Position": row.get("position", 0),
                }
                data.append(entry)

            df = pd.DataFrame(data)
            df.to_csv(f"search_console_report2{datetime.date.today()}.csv", index=False)
            print(f"Report saved as search_console_report{datetime.date.today()}.csv")
        else:
            print("No data found for the given date range.")
    else:
        if "rows" in response:
            data = []
            for row in response["rows"]:
                entry = {
                    "Query": row["keys"][0] if len(row["keys"]) > 0 else None,
                    "Clicks": row.get("clicks", 0),
                    "Impressions": row.get("impressions", 0),
                    "CTR": row.get("ctr", 0),
                    "Position": row.get("position", 0),
                }
                data.append(entry)

            df = pd.DataFrame(data)
            return df
        else:
            print("No data found for the given date range.")

#Setup Logging
logging.basicConfig(filename="gsc_report.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def main(site_url = SITE_URL, flag = True):
    logging.info("Start Log")
    try:
        fetch_search_console_datav1(site_url, flag)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
    logging.info("End Log")
#EOF