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
        events = []

        embedded = data.get("_embedded", {}).get("events", [])

        for e in embedded:
            events.append({
                "title": e.get("name"),
                "date": e.get("dates", {}).get("start", {}).get("localDate"),
                "time": e.get("dates", {}).get("start", {}).get("localTime"),
                "venue": self._get_venue(e),
                "url": e.get("url"),
            })

        return events

    def _get_venue(self, event):
        venues = event.get("_embedded", {}).get("venues", [])
        if venues:
            return venues[0].get("name")
        return "Unknown venue"