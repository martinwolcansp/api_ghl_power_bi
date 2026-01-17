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


def paginated_get(endpoint: str, params: dict, data_key: str):
    results = []
    page = 1

    while True:
        params.update({
            "location_id": LOCATION_ID,
            "page": page,
            "limit": 100
        })

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


def get_opportunities(start_date=None, end_date=None):
    params = {}
    if start_date:
        params["createdAt[gte]"] = start_date
    if end_date:
        params["createdAt[lte]"] = end_date

    return paginated_get(
        endpoint="/opportunities/search",
        params=params,
        data_key="opportunities"
    )


def get_contacts(start_date=None, end_date=None):
    params = {}
    if start_date:
        params["createdAt[gte]"] = start_date
    if end_date:
        params["createdAt[lte]"] = end_date

    return paginated_get(
        endpoint="/contacts/",
        params=params,
        data_key="contacts"
    )
