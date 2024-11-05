from django.urls import path

from hangar.views import (
    index,
    UserCreationView,
    UserProfileView,
    # AirplaneCreateView,
    AirplaneListView,
    # astronaut_list_view,
    flight_list_view,
    # FlightCreateView,
    FlightDetailView,
    # AstronautCreateView,
    AirplaneDetailView,
    # AstronautDetailView,
)

urlpatterns = [
    path("", index, name="main-page"),
    path("registration/", UserCreationView.as_view(), name="registration"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("airplanes/", AirplaneListView.as_view(), name="Airplane-list"),
    # path("airplanes/create/", AirplaneCreateView.as_view(), name="Airplane-create"),
    path("airplanes/<int:pk>/details/", AirplaneDetailView.as_view(), name="Airplane-details"),
    # path("astronauts/", astronaut_list_view, name="astronaut-list"),
    # path("astronauts/create/", AstronautCreateView.as_view(), name="astronaut-create"),
    # path("astronauts/<int:pk>/details/", AstronautDetailView.as_view(), name="astronaut-details"),
    path("flights/", flight_list_view, name="flight-list"),
    # path("flights/create/", FlightCreateView.as_view(), name="flight-create"),
    path("flights/<int:pk>/details/", FlightDetailView.as_view(), name="flight-details"),
]

app_name = "hangar"
