import requests
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.locations_query_url = "https://api.tequila.kiwi.com/locations/query"
        self.flight_deals_google_sheet_url = "https://api.sheety.co/547348702ffd55fd2956708f5dfbba08/flightDeals/prices"
        self.tequila_api = os.environ.get("TEQUILA_API")
        self.headers = dict(apikey=self.tequila_api, accept="application/json")
        self.cities = self.gather_cities_from_google_sheet()

    def get_iata_code(self, term):
        parameters = dict(term=term, locale="en-US", location_types="airport", limit=1, active_only="true")
        response = requests.get(url=self.locations_query_url, headers=self.headers, params=parameters)
        response.raise_for_status()
        iata = response.json()["locations"][0]["city"]["code"]
        print(iata)
        return iata

    def update_iata_code(self, term, sheet_id):
        pass

    def gather_cities_from_google_sheet(self):
        sheety_header = {
            "Authorization": os.environ.get("FLIGHTS_BEAR")
        }
        response = requests.get(url=self.flight_deals_google_sheet_url, headers=sheety_header)
        response.raise_for_status()
        print(response.json())
        city_list = [response.json()["prices"]][0]
        print(f"city list = {city_list}")
        return city_list

    def check_ita_code(self, city_list):
        for site in city_list:
            city = site["city"]
            sheet_id = site['id']
            print(city, sheet_id)
            try:
                iata = site['iata']
                print(site['iata'])
            except KeyError:
                print(f"{city} has no IATA info")
                site['iata'] = self.get_iata_code(city)
                self.update_iata_code(city, sheet_id)


test = DataManager()
for destination in test.cities:
    test.get_iata_code(destination)
