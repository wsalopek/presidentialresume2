import requests
import os
import json

CONGRESS = '118'
BASE_URL = 'https://api.congress.gov/v3/member'
HEADERS = {'User-Agent': 'presidentialresume.com'}

def fetch_chamber(chamber):
    url = f"{BASE_URL}/{chamber}?congress={CONGRESS}&limit=250"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get('members', [])

def save_members(members, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(members, f, indent=2)

def main():
    os.makedirs("data", exist_ok=True)

    house_members = fetch_chamber('house')
    save_members(house_members, 'data/house_members.json')

    senate_members = fetch_chamber('senate')
    save_members(senate_members, 'data/senate_members.json')

    print(f"✅ Saved {len(house_members)} House and {len(senate_members)} Senate members.")

if __name__ == '__main__':
    main()
