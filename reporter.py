import ga4
import search_console
import datetime
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension

#####################################################################################
#Path to service account JSON key file
SERVICE_ACCOUNT_FILE = "seo-reporting-454814-f0764e15f27c.json"

#Google Analytics Property ID
PROPERTY_ID = "258231506"

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
    "dimensions": ["page"], 
    "rowLimit": 25000,  
}

####################################################################################

#for holding data temporarily
data = []

def main():
    #GA4
    ga4.run_ga_report()

    #Search Console
    search_console.fetch_search_console_datav1()
    return()

if __name__ == "__main__":
    main()