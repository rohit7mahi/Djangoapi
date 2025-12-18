from django.urls import path
from .views import health_check, route_planner

urlpatterns = [
    path('health/', health_check),
    path('route/', route_planner),
]
