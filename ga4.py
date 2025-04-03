import json
import datetime
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension
from google.oauth2 import service_account

#Path to service account JSON key file
SERVICE_ACCOUNT_FILE = "seo-reporting-454814-f0764e15f27c.json"

#Google Analytics Property ID
PROPERTY_ID = "258231506"
B10_PROPERTY_ID = "434242361"
CINCY_PROPERTY_ID = "382980936"
KSTATE_PROPERTY_ID = "382989191"
PITT_PROPERTY_ID = "44221364"
TULSA_PROPERTY_ID = "469867835"
WESTERN_PROPERTY_ID = "452017641"
SUMMIT_PROPERTY_ID = "474017266"

#Set the date range
DATE_RANGE = DateRange(start_date="9daysAgo", end_date="yesterday")

#Set the metrics we want to grab
METRICS = [
    Metric(name="sessions"),   #Sessions
    Metric(name="purchaseRevenue")  #Revenue
]

#Set the filter to organic traffic
DIMENSIONS = [Dimension(name="sessionDefaultChannelGroup")]

def get_organic_data(property_id):
    #Create a Google Analytics client
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    client = BetaAnalyticsDataClient(credentials=credentials)

    #Fetches organic sessions and revenue from Google Analytics.
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DATE_RANGE],
        dimensions=DIMENSIONS,
        metrics=METRICS
    )

    response = client.run_report(request)

    #Extract data
    data = []
    for row in response.rows:
        channel = row.dimension_values[0].value
        if channel.lower() == "organic search":  #Filter organic traffic
            sessions = row.metric_values[0].value
            revenue = row.metric_values[1].value
            data.append({"Property":property_id, "Channel": channel, "Sessions": sessions, "Revenue": revenue})

    return data

def save_to_csv(data, filename= f"ga4{datetime.date.today()}.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def run_ga_report(property_id, flag=False):
    analytics_data = get_organic_data(property_id)
    if analytics_data and not flag:
        save_to_csv(analytics_data)
    if analytics_data and flag:
        return(analytics_data)
    else:
        print(f"No organic traffic data found for {property_id}.")

if __name__ == "__main__":
    run_ga_report(B10_PROPERTY_ID)