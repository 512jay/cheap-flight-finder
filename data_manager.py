import requests
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.flight_deals_google_sheet_url = "https://api.sheety.co/547348702ffd55fd2956708f5dfbba08/flightDeals/prices"
        self.sheety_header = dict(Authorization=os.environ.get("FLIGHTS_BEAR"))
        self.locations_query_url = "https://api.tequila.kiwi.com/locations/query"
        self.tequila_api = os.environ.get("TEQUILA_API")
        self.tequila_header = dict(apikey=self.tequila_api, accept="application/json")
        self.cities = self.gather_cities_from_google_sheet()
        self.check_iata_code()
        self.load_destinations()
        self.city_list = self.cities

    def get_iata_code(self, term):
        """Given a term like a city it returns the IATA code"""

        parameters = dict(term=term, locale="en-US", location_types="airport", limit=1, active_only="true")
        response = requests.get(url=self.locations_query_url, headers=self.tequila_header, params=parameters)
        response.raise_for_status()
        iata = response.json()["locations"][0]["city"]["code"]
        return iata

    def update_iata_code(self, sheet_id, iata):
        """Updates the Google sheet with the IATA"""
        update_data = {
            "price": {
                "iata": iata
            }
        }
        response = requests.put(url=f"{self.flight_deals_google_sheet_url}/{sheet_id}",
                                headers=self.sheety_header, json=update_data)
        response.raise_for_status()

    def gather_cities_from_google_sheet(self):
        """Returns a dictionary of cities along id and IATA (if available) from Google sheets"""
        response = requests.get(url=self.flight_deals_google_sheet_url, headers=self.sheety_header)
        response.raise_for_status()
        city_list = [response.json()["prices"]][0]
        return city_list

    def check_iata_code(self):
        """Checks if the dictionary of cites all have IATA codes"""
        for site in self.cities:
            city = site["city"]
            sheet_id = site['id']
            try:
                if len(site['iata']) != 3:
                    print(f"{city} has an invalid IATA field attempting update")
                    site['iata'] = self.get_iata_code(city)
                    self.update_iata_code(sheet_id, site['iata'])
            except KeyError:
                print(f"{city} has no IATA info attempting update")
                site['iata'] = self.get_iata_code(city)
                self.update_iata_code(sheet_id, site['iata'])

    def load_destinations(self):
        for destination in self.cities:
            self.get_iata_code(destination)

    def get_list(self):
        return self.city_list
