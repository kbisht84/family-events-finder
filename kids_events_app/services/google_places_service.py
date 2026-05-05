import requests
from django.conf import settings


class GooglePlacesService:
    PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(self):
        self.api_key_places = settings.GOOGLE_PLACES_API_KEY
        self.api_key_geo_code = settings.GOOGLE_GEOCODING_API_KEY

    def get_places(self, lat, lon, radius=10000, place_type=None):
        params = {
            "location": f"{lat},{lon}",
            "radius": radius,
            "key": self.api_key_places
        }

        # Optional filtering by type
        if place_type:
            params["type"] = place_type  # e.g., park, museum, zoo

        response = requests.get(self.PLACES_URL, params=params, timeout=5)
        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        if response.status_code != 200:
            print("Google API error:", response.text)
            return []

        data = response.json()
        return self._format_results(data.get("results", []))

    def get_places_by_zip(self, zip_code, radius=10000, place_type=None):
        lat, lon = self._get_lat_lon_from_zip(zip_code)

        print("ZIP → LAT/LON:", lat, lon)  # debug

        if not lat or not lon:
            return []

        return self.get_places(lat, lon, radius, place_type)

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

    def _get_lat_lon_from_zip(self, zip_code):
        params = {
            "address": zip_code,
            "key": self.api_key_geo_code
        }

        try:
            response = requests.get(self.GEOCODE_URL, params=params, timeout=5)
            print("GEOCODE STATUS:", response.status_code)
            print("GEOCODE RAW:", response.text[:300])  # debug

            if response.status_code != 200:
                return None, None

            data = response.json()

            # Check API-level status
            if data.get("status") != "OK":
                print("GEOCODE ERROR:", data.get("status"), data.get("error_message"))
                return None, None

            results = data.get("results", [])
            if not results:
                return None, None

            location = results[0]["geometry"]["location"]

            lat = location.get("lat")
            lon = location.get("lng")

            print("ZIP:", zip_code, "→ LAT/LON:", lat, lon)

            return lat, lon

        except Exception as e:
            print("GEOCODE EXCEPTION:", str(e))
            return None, None


