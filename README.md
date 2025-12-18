# Djangoapi

# Fuel Route Planner API

## Overview
This Django REST API calculates real driving distance and fuel cost between two locations.

## Features
- Real driving distance using OpenRouteService
- Fuel prices loaded from CSV
- Cheapest fuel stop selection
- Minimal external API calls
- Fast response time

## Tech Stack
- Django
- Django REST Framework
- OpenRouteService API

## API Endpoint

GET /api/route/?start=<city>&end=<city>

Example:
GET /api/route/?start=Los+Angeles&end=Las+Vegas

## Response
Returns distance, fuel stops, fuel gallons, and total fuel cost.

## Setup
1. Create virtual environment
2. Install dependencies
3. Add OpenRouteService API key
4. Run server
