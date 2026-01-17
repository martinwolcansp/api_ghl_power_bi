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


def paginated_get(endpoint: str, data_key: str):
    results = []
    page = 1

    while True:
        params = {
            "location_id": LOCATION_ID,
            "page": page,
            "limit": 100
        }

        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=HEADERS,
            params=params
        )

        if response.status_code != 200:
            raise Exception(f"GHL API error {response.status_code}: {response.text}")

        data = response.json()
        items = data.get(data_key, [])

        if not items:
            break

        results.extend(items)
        page += 1

    return results


def get_opportunities():
    return paginated_get(
        endpoint="/opportunities/search",
        data_key="opportunities"
    )


def get_contacts():
    return paginated_get(
        endpoint="/contacts/",
        data_key="contacts"
    )
