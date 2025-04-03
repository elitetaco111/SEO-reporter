import ga4
import search_console
import datetime
import pandas as pd
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension

#####################################################################################
#Path to service account JSON key file
SERVICE_ACCOUNT_FILE = "seo-reporting-454814-f0764e15f27c.json"

#Google Analytics Property ID
PROPERTY_ID = "258231506"
B10_PROPERTY_ID = "434242361"
CINCY_PROPERTY_ID = "382980936"
KSTATE_PROPERTY_ID = "382989191"
PITT_PROPERTY_ID = "442213164"
TULSA_PROPERTY_ID = "469867835"
WESTERN_PROPERTY_ID = "452017641"
#Breaks the script, no data found for Summit
SUMMIT_PROPERTY_ID = "474017266"

#Set the date range to grab data from GA4
DATE_RANGE = DateRange(start_date="9daysAgo", end_date="yesterday")

#Set the metrics we want to grab
METRICS = [
    Metric(name="sessions"),   #Sessions
    Metric(name="purchaseRevenue")  #Revenue
]
#Set the filter to organic traffic
DIMENSIONS = [Dimension(name="sessionDefaultChannelGroup")]

####################################################################################
#                   GA4 Globals Above                                              #
#                   Search Console Globals Below                                   #
####################################################################################

#Search Console Client Sercrets JSON file
CLIENT_SECRETS_FILE = "client_secret_473146300778-k68g02h1iqftcukodvm29j5clsn3num2.apps.googleusercontent.com.json" 

#Search Console API scope
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

#Set site url
SITE_URL = "https://www.rallyhouse.com" 

#Create the vars for date range for SC, 9 days ago to yesterday for Sun-Mon reports
date1 = datetime.date.today()
timedelta = datetime.timedelta(days=1)
date2 = date1 - timedelta #yesterday (cannot generate the report for today)
timedelta = datetime.timedelta(days=9)
date3 = date1 - timedelta #9 days ago to generate consistent sun-mon reports

START_DATE = date3.strftime("%Y-%m-%d") #start date
END_DATE = date2.strftime("%Y-%m-%d") #end date

#Build the request for search console
request = {
    "startDate": START_DATE,  #start date
    "endDate": END_DATE,    #end date (must be after or equal to start date)
    "dimensions": ["Query"], 
    "rowLimit": 25000,
    "orderBy":[
    {
      "field": "impressions",
      "order": "descending"
    }]  
}

####################################################################################

def concat_ga_data(data, result):
    df = pd.DataFrame(result)
    new_row = df.loc[0,["Property", "Channel", "Sessions", "Revenue"]]
    data.loc[len(data)] = new_row

def main():
    #GA4
    data = pd.DataFrame()
    count = 0
    properties = [PROPERTY_ID, B10_PROPERTY_ID, CINCY_PROPERTY_ID, KSTATE_PROPERTY_ID, TULSA_PROPERTY_ID, WESTERN_PROPERTY_ID, PITT_PROPERTY_ID]
    for property_id in properties:
        if count == 0:
            data = pd.DataFrame(ga4.run_ga_report(property_id, True))
            count += 1
        else:
            concat_ga_data(data, ga4.run_ga_report(property_id, True))

    ga4.save_to_csv(data)

    #Search Console
    urls = ["https://www.rallyhouse.com", "https://shop.bigtenstore.com", "https://shop.gobearcats.com", "https://shop.kstatesports.com", "https://shoppittpanthers.com", "https://shopgoldenhurricane.com", "https://shopwmubroncos.com"]
    num = 1
    for url in urls:
        sc = pd.DataFrame(search_console.fetch_search_console_datav1(url, False))
        sc.to_csv(f"search_console_report{datetime.date.today()}_{num}.csv", index=False)
        num += 1
    return()

if __name__ == "__main__":
    main()
#EOF