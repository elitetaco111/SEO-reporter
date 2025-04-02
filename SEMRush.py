import requests
import csv
import io
import datetime

# Configuration
API_KEY = "your_api_key"
DOMAIN = "example.com"
CSV_FILE = f"semrush_report_{datetime.date.today()}.csv"

# Fetch data from SEMrush API
def fetch_seo_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    print(f"Error: {response.status_code}, {response.text}")
    return None

# Parse SEMrush CSV API response into a dictionary
def parse_seo_data(response_text):
    reader = csv.reader(io.StringIO(response_text))
    headers = next(reader)
    data = next(reader)
    return dict(zip(headers, data))

# Get Site Health Score & Errors from SEMrush
def get_site_audit_data():
    url = f"https://api.semrush.com/?type=siteaudit_overview&key={API_KEY}&site={DOMAIN}&export=api"
    response_text = fetch_seo_data(url)
    return parse_seo_data(response_text) if response_text else {}

# Get Visibility Score from SEMrush
def get_visibility_data():
    url = f"https://api.semrush.com/?type=domain_ranks&key={API_KEY}&domain={DOMAIN}&export=api"
    response_text = fetch_seo_data(url)
    return parse_seo_data(response_text) if response_text else {}

# Save results to a CSV file with a timestamp
def save_to_csv(data):
    file_exists = False
    try:
        with open(CSV_FILE, "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Domain", "Health Score", "Errors", "Visibility Score"])
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            DOMAIN,
            data.get("Health Score", "N/A"),
            data.get("Errors", "N/A"),
            data.get("Visibility Score", "N/A")
        ])

# Main function to get SEO data and save it to CSV
def main():
    site_audit_data = get_site_audit_data()
    visibility_data = get_visibility_data()
    
    combined_data = {
        "Health Score": site_audit_data.get("site_health_score", "N/A"),
        "Errors": site_audit_data.get("errors", "N/A"),
        "Visibility Score": visibility_data.get("Rank", "N/A")
    }
    
    save_to_csv(combined_data)
    print("Report saved successfully!")

if __name__ == "__main__":
    main()
