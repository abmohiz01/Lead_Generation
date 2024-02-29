import json
from filtered_domains import domains_to_exclude


def load_json(path: str) -> dict | list:
    """
    Load a JSON file from the given path
    :param path:
    :return:
    """
    with open(path, "r") as file:
        return json.load(file)


def extract_urls_from_google_search_results(json_data: dict) -> dict:
    """
    Extract the URLs from the Google search results JSON
    :param json_data: data loaded from the Google search results JSON
    :return:
    """
    results = {}
    for business in json_data:
        if business.get("website"):
            results[business["name"]] = {
                "website": business["website"],
                "address": business.get("address", ""),
                "rating": business.get("rating", ""),
                "price_level": business.get("price_level", ""),
                "types": business.get("types", ""),
                "phone": business.get("phone", ""),
                "number_of_ratings": business.get("number of ratings", ""),
                "business_status": business.get("business_status", "")
            }
    return results


def check_url(url: str) -> bool:
    """
    Check if the url contains any invalid domains as substrings
    :param url: URL to check
    :return: True if the URL is valid, False otherwise
    """
    for invalid_domain in domains_to_exclude:
        if invalid_domain in url:
            return False
    return True


def filter_urls(urls: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """
    Filter the list of URLs to only include those from the given domain
    :param urls: list of URLs

    :return: list of URLs from the given domain
    """
    filtered_urls = {}
    for name, params in urls.items():
        if check_url(params["website"]):
            filtered_urls[name] = params
    return filtered_urls


def urls_to_crawl(json_file_to_load: str = 'google_restaurants_list.json') -> dict[str, dict[str, str]]:
    """
    Load the JSON file, extract the URLs from the Google search results, and filter them.
    :param json_file_to_load:
    :return: a dictionary containing the name of the business as key and url of the website as value
    """
    json_data = load_json(json_file_to_load)
    urls = extract_urls_from_google_search_results(json_data)
    filtered_urls = filter_urls(urls)


    with open('569_Filtered_URLS.json', 'w') as outfile:
        json.dump(filtered_urls, outfile, indent=4)
        return filtered_urls


if __name__ == "__main__":
    urls = urls_to_crawl()
    print(urls)
    print(len(urls))
