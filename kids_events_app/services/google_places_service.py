import requests
from django.conf import settings


class GooglePlacesService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    def __init__(self):
        self.api_key = settings.GOOGLE_PLACES_API_KEY

    def get_places(self, lat, lon, radius=10000, place_type=None):
        params = {
            "location": f"{lat},{lon}",
            "radius": radius,
            "key": self.api_key
        }

        # Optional filtering by type
        if place_type:
            params["type"] = place_type  # e.g., park, museum, zoo

        response = requests.get(self.BASE_URL, params=params, timeout=5)
        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        if response.status_code != 200:
            print("Google API error:", response.text)
            return []

        data = response.json()
        return self._format_results(data.get("results", []))

    def _format_results(self, results):
        places = []

        for p in results:
            places.append({
                "name": p.get("name"),
                "address": p.get("vicinity"),
                "rating": p.get("rating"),
                "lat": p.get("geometry", {}).get("location", {}).get("lat"),
                "lon": p.get("geometry", {}).get("location", {}).get("lng"),
            })

        return places


