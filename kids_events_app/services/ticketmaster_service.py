import requests
from django.conf import settings


class TicketmasterService:
    BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

    def __init__(self):
        self.api_key = settings.TICKETMASTER_API_KEY

    def get_events(self, city, start, end, keyword=None):
        params = {
            "apikey": self.api_key,
            "city": city,
            "startDateTime": f"{start}T00:00:00Z",
            "endDateTime": f"{end}T23:59:59Z",
            "size": 20,  # number of results
        }

        if keyword:
            params["keyword"] = keyword  # e.g., "family"

        print("Params: ", params)
        response = requests.get(self.BASE_URL, params=params, timeout=5)

        print("STATUS:", response.status_code)
        print("RAW:", response.text[:500])  # debug

        if response.status_code != 200:
            return []

        data = response.json()
        return self._format_events(data)

    def _format_events(self, data):
        normalized_events = []

        embedded = data.get("_embedded", {}).get("events", [])

        for e in embedded:
            venue = (
                e.get("_embedded", {})
                .get("venues", [{}])[0]
            )

            location = venue.get("location", {})
            normalized_events.append({
                "title": e.get("name"),
                "date": e.get("dates", {}).get("start", {}).get("localDate"),
                "time": e.get("dates", {}).get("start", {}).get("localTime"),
                "venue": venue.get("name"),
                "address": venue.get("address", {}).get("line1"),
                "lat": location.get("latitude"),
                "lon": location.get("longitude"),
                "url": e.get("url"),
                "image": e.get("images", [{}])[0].get("url"),
            })

        return normalized_events