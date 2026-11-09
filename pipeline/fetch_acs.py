import json
import os
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

# --- Settings ---
YEAR = 2024
TABLE = "B22003"
VARIABLES = ["NAME", "B22003_001E", "B22003_001M", "B22003_002E", "B22003_002M"]
URL = f"https://api.census.gov/data/{YEAR}/acs/acs5"
RAW_DIR = Path("raw")

GEOGRAPHIES = {
    "house":  {"for": "state legislative district (lower chamber):*", "in": "state:15"},
    "senate": {"for": "state legislative district (upper chamber):*", "in": "state:15"},
    "county": {"for": "county:*", "in": "state:15"},
    "state":  {"for": "state:15"},
}




load_dotenv()
#Look at .env.example file, and creatte your own private .env file with the api key. Do not commit your .env file to git, it is private.
# reads .env and loads its lines into the environment
key = os.environ["CENSUS_API_KEY"]     # grab the value by name from  .env


# --- Download each geography and save it ---
for geo_name, geo_params in GEOGRAPHIES.items():
    params = {
        "get": ",".join(VARIABLES),   # turns the list into "NAME,B22003_001E,..."
        "key": key,
        **geo_params,                  # adds the "for"/"in" entries from above
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()        # crash if Census returned an error
    rows = response.json()

    receipt = {
        "retrieved_at": date.today().isoformat(),
        "table": TABLE,
        "year": YEAR,
        "geography": geo_name,
        "rows": rows,
    }

    out_path = RAW_DIR / f"acs_{TABLE}_{geo_name}.json"
    out_path.write_text(json.dumps(receipt, indent=2))
    print(f"Saved {len(rows) - 1} rows to {out_path}")