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
    """
    Obtiene oportunidades sin parámetros adicionales
    """
    response = requests.get(
        f"{BASE_URL}/opportunities/search",
        headers=HEADERS,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"GHL API error {response.status_code}: {response.text}"
        )

    return response.json().get("opportunities", [])


def get_contacts(limit: int = 100):
    """
    Obtiene contactos usando Private Integration API Key
    (misma lógica que prueba local)
    """
    response = requests.get(
        f"{BASE_URL}/contacts/",
        headers=HEADERS,
        params={
            "locationId": LOCATION_ID,
            "limit": limit
        },
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"GHL API error {response.status_code}: {response.text}"
        )

    return response.json().get("contacts", [])
