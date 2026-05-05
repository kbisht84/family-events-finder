import requests
from django.conf import settings


class EventbriteService:
    BASE_URL = "https://www.eventbriteapi.com/v3/events/search"

    def __init__(self):
        self.token = settings.EVENTBRITE_API_TOKEN

    def get_events(self, start, end, zip_code):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        params = {
            "location.address": zip_code,
            "start_date.range_start": f"{start}T00:00:00Z",
            "start_date.range_end": f"{end}T23:59:59Z",
            "expand": "venue",
        }

        response = requests.get(self.BASE_URL, headers=headers, params=params, timeout=5)

        print(response.status_code, response.text)

        if response.status_code != 200:
            return []

        data = response.json()
        return self._format_events(data.get("events", []))

    def _filter_kids_events(self, events):
        keywords = ["kids", "children", "family", "toddler"]

        filtered = []

        for event in events:
            name = event.get("name", {}).get("text", "") or ""
            description = event.get("description", {}).get("text", "") or ""

            combined = (name + " " + description).lower()

            if any(keyword in combined for keyword in keywords):
                filtered.append({
                    "title": name,
                    "start": event.get("start", {}).get("local"),
                    "end": event.get("end", {}).get("local"),
                    "venue": event.get("venue", {}).get("address", {}).get("localized_address_display") if event.get("venue") else None,
                    "url": event.get("url"),
                })

        return filtered

    def _format_events(self, events):
        formatted = []

        for event in events:
            formatted.append({
                "title": event.get("name", {}).get("text"),
                "description": event.get("description", {}).get("text"),
                "start": event.get("start", {}).get("local"),
                "end": event.get("end", {}).get("local"),
                "url": event.get("url"),
                "venue": self._get_venue(event),
            })

        return formatted

    def _get_venue(self, event):
        venue = event.get("venue")
        if not venue:
            return None

        return venue.get("address", {}).get("localized_address_display")