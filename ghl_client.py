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
    Obtiene oportunidades sin filtros adicionales
    """
    results = []
    page = 1

    while True:
        # ⚠️ Payload NUEVO por iteración (evita contaminación)
        payload = {
            "locationId": LOCATION_ID,
            "limit": 100,
            "page": page
        }

        # 🔒 Blindaje por si el dict viene contaminado
        payload.pop("search_after", None)

        response = requests.post(
            f"{BASE_URL}/opportunities/search",
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        if response.status_code not in (200, 201):
            raise Exception(
                f"GHL API error {response.status_code}: {response.text}"
            )

        data = response.json()
        opportunities = data.get("opportunities", [])

        if not opportunities:
            break

        results.extend(opportunities)
        page += 1

    return results


def get_contacts(limit: int = 100):
    results = []

    last_start_after = None
    last_start_after_id = None

    while True:
        params = {
            "locationId": LOCATION_ID,
            "limit": limit
        }

        if last_start_after and last_start_after_id:
            params["startAfter"] = last_start_after
            params["startAfterId"] = last_start_after_id

        # 🔍 DEBUG CLAVE (ACÁ)
        print(
            "PARAMS >>>",
            params,
            {k: type(v) for k, v in params.items()}
        )

        response = requests.get(
            f"{BASE_URL}/contacts",
            headers=HEADERS,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(
                f"GHL API error {response.status_code}: {response.text}"
            )

        data = response.json()
        contacts = data.get("contacts", [])
        meta = data.get("meta", {})

        if not contacts:
            break

        results.extend(contacts)

        if not meta.get("startAfter") or not meta.get("startAfterId"):
            break

        last_start_after = f"{meta['startAfter']}"
        last_start_after_id = f"{meta['startAfterId']}"

    return results



