import os
import requests
import json

API_BASE = "https://api.congress.gov/v3/member"
CONGRESS = 118  # You can update this as needed

# Read the API key from the environment variable
API_KEY = os.getenv("CONGRESS_API_KEY")

HEADERS = {
    "X-API-Key": API_KEY
}

def fetch_chamber(chamber):
    url = f"{API_BASE}/{chamber}?congress={CONGRESS}&limit=250"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("members", [])

def save_json(data, filename):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{filename}", "w") as f:
        json.dump(data, f, indent=2)

def main():
    print("📥 Fetching House members...")
    house_members = fetch_chamber("house")
    save_json(house_members, "house_members.json")
    print(f"✅ Saved {len(house_members)} House members.")

    print("📥 Fetching Senate members...")
    senate_members = fetch_chamber("senate")
    save_json(senate_members, "senate_members.json")
    print(f"✅ Saved {len(senate_members)} Senate members.")

if __name__ == "__main__":
    main()

