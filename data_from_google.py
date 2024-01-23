import json
import pandas as pd

with open('west_virginia_restaurants.json') as f:
    data = json.load(f)

required_data_list = []
for restaurant in data:
    required_data = {
        "name": restaurant.get("name", "N/A"),
        "address": restaurant.get("vicinity", "N/A"),
        "rating": restaurant.get("rating", "N/A"),
        "price_level": restaurant.get("price_level", "N/A"),
        "types": ", ".join(_type for _type in restaurant["types"] if "types" in restaurant),
        "website": restaurant.get("website", "N/A"),
        "phone": restaurant.get("formatted_phone_number", "N/A"),
        "number of ratings": restaurant.get("user_ratings_total", "N/A"),
        "business_status": restaurant.get("business_status", "N/A"),
    }
    required_data_list.append(required_data)

with open('google_restaurants_list.json', 'w') as f:
    json.dump(required_data_list, f, indent=4)


df = pd.DataFrame(required_data_list)
df.to_csv('google_restaurants_list.csv', index=False)