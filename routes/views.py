from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import calculate_fuel_gallons, select_fuel_stops

from .utils import (
    calculate_fuel_gallons,
    select_fuel_stops,
    get_route_distance
)

@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "API is working"
    })


@api_view(['GET'])
def route_planner(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    if not start or not end:
        return Response(
            {"error": "start and end locations are required"},
            status=400
        )

    distance_miles = get_route_distance(start, end)

    fuel_gallons = calculate_fuel_gallons(distance_miles)
    fuel_stops = select_fuel_stops(distance_miles)

    total_fuel_cost = round(
        sum(stop["price"] for stop in fuel_stops) * fuel_gallons,
        2
    )

    return Response({
        "start": start,
        "end": end,
        "distance_miles": distance_miles,
        "fuel_stops": fuel_stops,
        "total_fuel_gallons": fuel_gallons,
        "total_fuel_cost_usd": total_fuel_cost
    })


