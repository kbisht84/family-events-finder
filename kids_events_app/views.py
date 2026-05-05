from django.shortcuts import render
from datetime import datetime
from .utils import Calendar
from django.http import JsonResponse
from .services.eventbrite_service import EventbriteService
from .services.google_places_service import GooglePlacesService
from .services.ticketmaster_service import TicketmasterService


def calendar_view(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    now = datetime.now()
    year = int(year) if year else now.year
    month = int(month) if month else now.month

    cal = Calendar(year, month).formatmonth()


    return render(request, 'kids_events_app/calendar.html', {
        'calendar': cal,
        'month': month,
        'year': year,
        'months': list(range(1, 13)),
        'years': list(range(2020, 2031)),  # adjust range
    })

def get_data(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    zip_code = request.GET.get('zip')

    if not zip_code:
        return JsonResponse({"error": "ZIP code required"}, status=400)

    service = EventbriteService()

    # events pulling from eventbrite
    events = service.get_events(start, end, zip_code)

    return JsonResponse({
        "events": events
    })

def get_places(request):
    zip_code = request.GET.get("zip")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    place_type = request.GET.get("type")  # optional

    service = GooglePlacesService()
    # Priority: ZIP → fallback to lat/lon
    if zip_code:
        places = service.get_places_by_zip(zip_code, place_type=place_type)
    elif lat and lon:
        places = service.get_places(lat, lon, place_type=place_type)
    else:
        return JsonResponse({"error": "Location required"}, status=400)

    return JsonResponse({"places": places})

def get_events(request):
    start = request.GET.get("start")
    end= request.GET.get("end")
    city = request.GET.get("city")
    keyword = request.GET.get("keyword")  # optional

    # start = format_date(start_raw) if start_raw else None
    # end = format_date(end_raw) if end_raw else None

    if not city:
        return JsonResponse({"error": "City required"}, status=400)

    service = TicketmasterService()
    events = service.get_events(city, start, end, keyword)

    return JsonResponse({"events": events})

def format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
# Create your views here.
