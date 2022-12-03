# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.
from flight_search import FlightSearch
from data_manager import DataManager

destinations = DataManager()
trip = FlightSearch()
places = destinations.city_list
for place in places:
    print(f"{place['city']} ${trip.search(place['iata'])['price']}")
