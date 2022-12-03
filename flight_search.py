import os
import requests
from datetime import datetime, timedelta


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.tequila_api = os.environ.get("TEQUILA_API")
        self.tequila_header = dict(apikey=self.tequila_api, accept="application/json")
        self.tequila_url = "https://api.tequila.kiwi.com/v2/search"

    def search(self, fly_to, fly_from="WAS"):
        """Gets the cheapest price for the next 6 months"""
        today = datetime.now()
        date_from = today.strftime("%d/%m/%Y")
        date_to = (today + timedelta(days=180)).strftime("%d/%m/%Y")
        payload = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "dateFrom": date_from,
            "dateTo": date_to,
            "curr": "USD",
            "locale": "en",
        }
        response = requests.get(url=self.tequila_url, headers=self.tequila_header, params=payload)
        response.raise_for_status()
        flights = response.json()["data"]
        if len(flights) > 0:
            cheapest_flight = flights[0]
            lowest_price = cheapest_flight["price"]
            for flight in flights:
                if flight["price"] < lowest_price:
                    lowest_price = flight["price"]
                    cheapest_flight = flight
            print(cheapest_flight["price"])
            return cheapest_flight
        return 9999999


trip = FlightSearch()
places = ["CUN", "LON", "ELP", "PAR", "NYC", "HOU"]
for place in places:
    print(f"{place} ${trip.search(place)['price']}")
