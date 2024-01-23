from yelpapi import YelpAPI
import csv


def get_all_restaurants(api_key, location):
    yelp_api = YelpAPI(api_key)
    offset = 0
    limit = 50
    total = None
    all_restaurants = []

    while total is None or offset < total:
        response = yelp_api.search_query(term='restaurants', location=location, limit=limit, offset=offset)
        restaurants = response.get('businesses', [])
        total = response.get('total', 0)
        all_restaurants.extend(restaurants)

        offset += limit

    return all_restaurants


# Extract and format restaurant data
def extract_restaurant_data(restaurants):
    restaurant_data = []
    for r in restaurants:
        data = {
            'name': r['name'],
            'address': ' '.join(r['location']['display_address']),
            'phone': r.get('phone', 'N/A')
        }
        restaurant_data.append(data)
    return restaurant_data


def dump_to_csv(data, filename):
    # Define the column headers for the CSV file
    headers = ['name', 'address', 'phone']

    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write the restaurant data
        for row in data:
            writer.writerow(row)

# Example usage
api_key = '_lbF85TxKopxa_X2M7D_Uh1wDmUeHNYVHIyK6fDqOVLd3KBzPddlJVjuEUwWQZTuv4mdMsrHCBD3azSuBiGaDO_nZQBg0hQVYW0O8RcNoXO5wix5irlH4DmjBGapZXYx'
all_restaurants = get_all_restaurants(api_key, 'West Virginia')
formatted_data = extract_restaurant_data(all_restaurants)

dump_to_csv(formatted_data, 'west_virginia_restaurants.csv')
print(len(formatted_data))