import json
from urllib.parse import urlparse
from publicsuffixlist import PublicSuffixList
import re

# Load the crawled data

with open('Pre_crawled_emails.json', 'r') as file:
    crawled_data = json.load(file)

psl = PublicSuffixList()

def extract_domain(url):
    """
    Extracts the primary domain from a URL, even if it's a subdomain.
    """
    netloc = urlparse(url).netloc
    # Use PublicSuffixList to get the correct domain from a URL
    domain = psl.privatesuffix(netloc)
    return domain if domain else netloc  # Fallback to netloc if domain extraction fails

def should_exclude_email(email):
    """
    Checks if the given email matches any of the patterns that should be excluded.
    """
    excluded_patterns = [r"@domain\.com$", r"your@mail\.com", r"@godaddy\.com$"]
    return any(re.search(pattern, email) for pattern in excluded_patterns)

def process_crawled_data(crawled_data):
    domain_emails = {}

    for item in crawled_data:
        url = item.get('url')
        email = item.get('email')
        if should_exclude_email(email):
            continue  # Skip unwanted emails

        normalized_domain = extract_domain(url)

        if normalized_domain not in domain_emails:
            domain_emails[normalized_domain] = set()

        domain_emails[normalized_domain].add(email)

    # Convert sets to lists for JSON serialization
    for domain in domain_emails:
        domain_emails[domain] = list(domain_emails[domain])

    return domain_emails

# Process the crawled data
processed_data = process_crawled_data(crawled_data)

# Save the processed data to a new JSON file
with open('processed_crawled_data.json', 'w') as file:
    json.dump(processed_data, file, indent=4)
