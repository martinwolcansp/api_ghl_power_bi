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


def get_contacts(limit=100, max_loops=5):
    """
    Fuerza requests SIN cursor para evitar search_after.
    Repite llamadas 'primera página' y deduplica.
    """
    results = {}
    loops = 0

    while loops < max_loops:
        response = requests.get(
            f"{BASE_URL}/contacts",
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

        contacts = response.json().get("contacts", [])

        if not contacts:
            break

        # deduplicación por id
        for c in contacts:
            results[c["id"]] = c

        loops += 1

    return list(results.values())


