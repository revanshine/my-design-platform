import os
import requests
import datetime
import time

API = "https://services.nvd.nist.gov/rest/json"
KEY = os.getenv("NVD_API_KEY")  # Set this in your environment for higher rate-limit

# Use timezone-aware datetimes
now = datetime.datetime.now(datetime.timezone.utc)
DAYS_BACK = 7   # Change this to whatever lookback you want
since = (now - datetime.timedelta(days=DAYS_BACK)).isoformat()
until = now.isoformat()

params = {
    "pubStartDate": since,
    "pubEndDate": until,
    "resultsPerPage": 20,
    "keywordSearch": "discord"
}
if KEY:
    params["apiKey"] = KEY

r = requests.get(f"{API}/cves/2.0", params=params, timeout=30)

if r.status_code != 200:
    print(f"API Error {r.status_code}: {r.headers.get('message', 'Unknown error')}")
    print(f"Response: {r.text}")
    exit(1)

try:
    data = r.json()
    vulns = data.get("vulnerabilities", [])
    print(f"Found {len(vulns)} CVEs for Discord in the last {DAYS_BACK} days:")
    for item in vulns:
        cve_id = item["cve"]["id"]
        desc = item["cve"]["descriptions"][0]["value"]
        print(f"{cve_id}: {desc[:100]}...")
except Exception as e:
    print(f"Failed to parse response: {e}")

# Sleep if doing more queries (to avoid NVD rate-limit)
time.sleep(6)
