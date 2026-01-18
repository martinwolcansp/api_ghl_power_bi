import requests
import os

BASE_URL = "https://services.leadconnectorhq.com"

API_KEY = os.getenv("GHL_API_KEY")
LOCATION_ID = os.getenv("GHL_LOCATION_ID")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}


def get_opportunities():
    results = []
    page = 1

    while True:
        params = {
            "location_id": LOCATION_ID,
            "page": page,
            "limit": 100
        }

        response = requests.get(
            f"{BASE_URL}/opportunities/search",
            headers=HEADERS,
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"GHL API error {response.status_code}: {response.text}")

        data = response.json()
        opps = data.get("opportunities", [])

        if not opps:
            break

        results.extend(opps)
        page += 1

    return results


def get_contacts():
    results = []
    start_after_id = None

    while True:
        params = {
            "locationId": LOCATION_ID,
            "limit": 100
        }

        if start_after_id:
            params["startAfterId"] = start_after_id

        response = requests.get(
            f"{BASE_URL}/contacts/",
            headers=HEADERS,
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"GHL API error {response.status_code}: {response.text}")

        data = response.json()
        contacts = data.get("contacts", [])

        if not contacts:
            break

        results.extend(contacts)

        start_after_id = data.get("meta", {}).get("startAfterId")
        if not start_after_id:
            break

    return results
