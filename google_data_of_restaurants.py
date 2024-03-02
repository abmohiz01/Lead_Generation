'''Module of API Call from Google API for restaurants in West Virginia'''
import csv
import json
import requests


def fetch_place_details(api_key: str, place_id: str):
    """Get the details of each restaurant given its place_id.

    :param api_key: google place api key
    :param place_id: unique place id for each restaurant
    :return: json response of the details of each restaurant
    """
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'formatted_phone_number,website',
        'key': api_key
    }
    response = requests.get(details_url, params=params)
    if response.status_code != 200:
        return None
    return response.json().get('result', {})


def fetch_nearby_restaurants(api_key: str, location, radius: int = 20000, page_token: str | None = None):
    """ Fetch nearby restaurants given a location

    :param api_key: unique api key for google places api.
    :param location: coordinates of the location.
    :param radius: in meters. default is 20km
    :param page_token: current page number of results.
    :return: list of restaurants and the next page token.
    """

    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,
        'radius': radius,
        'type': 'restaurant',
        'key': api_key
    }
    if page_token:
        params['pagetoken'] = page_token

    response = requests.get(endpoint_url, params=params)
    if response.status_code != 200:
        return None, None

    results = response.json()
    restaurants = results.get('results', [])
    for restaurant in restaurants:
        details = fetch_place_details(api_key, restaurant['place_id'])
        restaurant['formatted_phone_number'] = details.get('formatted_phone_number')
        restaurant['website'] = details.get('website')
    return restaurants, results.get('next_page_token')


def get_restaurants_for_counties(api_key: str, counties_coordinates: dict[str, str]):
    """ Get all restaurants for each county in West Virginia

    :param api_key: unique api key for google places api.
    :param counties_coordinates: list of counties and their coordinates.
    :return: list of restaurants where each restaurant is a dictionary.
    """
    all_restaurants = []
    seen_vicinities = set()

    for location in counties_coordinates.values():
        page_token = None
        while True:
            restaurants, page_token = fetch_nearby_restaurants(api_key, location, page_token=page_token)
            for restaurant in restaurants:
                if restaurant['vicinity'] not in seen_vicinities:
                    all_restaurants.append(restaurant)
                    seen_vicinities.add(restaurant['vicinity'])
            if not page_token:
                break
    return all_restaurants


# Example usage
counties_coordinates = {
    "Barbour County": "39.1399, -80.0088",
    "Berkeley County": "39.4562, -77.9645",
    "Boone County": "38.0179, -81.7166",
    "Braxton County": "38.7095, -80.7214",
    "Brooke County": "40.2715, -80.5660",
    "Cabell County": "38.4192, -82.4452",
    "Calhoun County": "38.8562, -81.1196",
    "Clay County": "38.4615, -81.0849",
    "Doddridge County": "39.2640, -80.7718",
    "Fayette County": "38.0308, -81.0907",
    "Gilmer County": "38.9218, -80.8560",
    "Grant County": "39.1064, -79.1998",
    "Greenbrier County": "37.9316, -80.4534",
    "Hampshire County": "39.3210, -78.6115",
    "Hancock County": "40.5074, -80.6094",
    "Hardy County": "39.0264, -78.8510",
    "Harrison County": "39.2818, -80.3792",
    "Jackson County": "38.8438, -81.6848",
    "Jefferson County": "39.3078, -77.8600",
    "Kanawha County": "38.3697, -81.6333",
    "Lewis County": "38.9938, -80.4999",
    "Lincoln County": "38.1751, -82.0850",
    "Logan County": "37.8393, -81.9748",
    "Marion County": "39.5096, -80.2281",
    "Marshall County": "39.8561, -80.6669",
    "Mason County": "38.7472, -82.0257",
    "McDowell County": "37.3934, -81.6646",
    "Mercer County": "37.4081, -81.1010",
    "Mineral County": "39.4196, -78.9412",
    "Mingo County": "37.7269, -82.1573",
    "Monongalia County": "39.6337, -80.0348",
    "Monroe County": "37.5794, -80.5451",
    "Morgan County": "39.5548, -78.2630",
    "Nicholas County": "38.2831, -80.7996",
    "Ohio County": "40.0664, -80.6042",
    "Pendleton County": "38.6838, -79.3733",
    "Pleasants County": "39.3868, -81.1657",
    "Pocahontas County": "38.3331, -80.0247",
    "Preston County": "39.4662, -79.6722",
    "Putnam County": "38.5258, -81.8603",
    "Raleigh County": "37.7693, -81.2370",
    "Randolph County": "38.7676, -79.8794",
    "Ritchie County": "39.2139, -81.0664",
    "Roane County": "38.7487, -81.3777",
    "Summers County": "37.6596, -80.8597",
    "Taylor County": "39.3348, -80.0435",
    "Tucker County": "39.1128, -79.5496",
    "Tyler County": "39.4570, -80.8723",
    "Upshur County": "38.9240, -80.2257",
    "Wayne County": "38.1497, -82.4249",
    "Webster County": "38.4892, -80.4328",
    "Wetzel County": "39.6004, -80.6337",
    "Wirt County": "39.0413, -81.3754",
    "Wood County": "39.2153, -81.5169",
    "Wyoming County": "37.6127, -81.5470"
}

API_KEY = 'AIzaSyD4JmOH9C7_WQ0bHoRWN-KxNVaMreG1Nw8'
restaurants = get_restaurants_for_counties(API_KEY, counties_coordinates)

with open('west_virginia_restaurants.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=restaurants[0].keys())

    # Write the header
    writer.writeheader()

    # Write the restaurant data
    for row in restaurants:
        writer.writerow(row)

with open('west_virginia_restaurants.json', mode='w', encoding='utf-8') as file:
    json.dump(restaurants, file)

print(len(restaurants))