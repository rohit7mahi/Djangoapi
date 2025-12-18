import requests
from django.conf import settings
import csv
import os
import math

MAX_RANGE_MILES = 500
MILES_PER_GALLON = 10


def load_fuel_prices():
    """
    Load fuel stations from fuel_prices.csv
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'fuel_prices.csv')

    stations = []

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                stations.append({
                    "truckstop_name": row["Truckstop Name"],
                    "city": row["City"],
                    "state": row["State"],
                    "price": float(row["Retail Price"])
                })
            except Exception:
                # Skip malformed rows
                continue

    return stations


def calculate_fuel_gallons(distance_miles):
    return round(distance_miles / MILES_PER_GALLON, 2)


def select_fuel_stops(distance_miles):
    stations = load_fuel_prices()
    stations = sorted(stations, key=lambda x: x["price"])

    stops_required = max(1, math.floor(distance_miles / MAX_RANGE_MILES))
    return stations[:stops_required]

def get_route_distance(start, end):
    geocode_url = "https://api.openrouteservice.org/geocode/search"
    route_url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }

    def geocode(place):
        response = requests.get(
            geocode_url,
            headers=headers,
            params={"text": place, "size": 1}
        )
        data = response.json()

        if "features" not in data or not data["features"]:
            raise Exception(f"Geocoding failed for {place}")

        return data["features"][0]["geometry"]["coordinates"]

    start_coords = geocode(start)
    end_coords = geocode(end)

    response = requests.post(
        route_url,
        headers=headers,
        json={"coordinates": [start_coords, end_coords]}
    )

    data = response.json()

    if "routes" not in data or not data["routes"]:
        raise Exception(f"Routing API error: {data}")

    distance_meters = data["routes"][0]["summary"]["distance"]
    distance_miles = distance_meters / 1609.34

    return round(distance_miles, 2)
