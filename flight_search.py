import os
import requests


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.tequila_api = os.environ.get("TEQUILA_API")
        self.tequila_header = dict(apikey=self.tequila_api, accept="application/json")
        self.tequila_url = "https://api.tequila.kiwi.com/v2/search"
        self.simple_search()

    def simple_search(self):
        payload = {
            "fly_from": "LGA",
            "fly_to": "MIA",
            "dateFrom": "02/12/2022",
            "dateTo": "02/05/2023",
            "curr": "USD",
            "locale": "en",
            "price_to": 150
        }
        response = requests.get(url=self.tequila_url, headers=self.tequila_header, params=payload)
        response.raise_for_status()
        flights = response.json()["data"]
        for flight in flights:
            print(flight["price"])


search = FlightSearch()
