import requests
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.locations_query_url = "https://api.tequila.kiwi.com/locations/query"
        self.tequila_api = os.environ.get("TEQUILA_API")
        self.headers = dict(apikey=self.tequila_api, accept="application/json")
        self.cities = self.gather_cities_from_google_sheet()

    def gather_cities_from_google_sheet(self):
        return ["Houston", "Dallas", "Paris", "London"]

    def get_international_air_transport_association_code(self, term):
        parameters = dict(term=term, locale="en-US", location_types="airport", limit=1, active_only="true")
        response = requests.get(url=self.locations_query_url, headers=self.headers, params=parameters)
        response.raise_for_status()
        iata = response.json()["locations"][0]["city"]["code"]
        print(iata)
        return iata


test = DataManager()
for city in test.cities:
    test.get_international_air_transport_association_code(city)
