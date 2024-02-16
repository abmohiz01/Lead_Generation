import json
from urllib.parse import urlparse
# Load the crawled data
with open('emails2.json', 'r') as file:
    crawled_data = json.load(file)

def process_crawled_data(crawled_data):
    domain_emails = {}

    for item in crawled_data:
        url = item.get('url')
        email = item.get('email')
        domain = urlparse(url).netloc

        # Normalize the domain by removing 'www.' or 'ww.'
        normalized_domain = domain.replace('www.', '').replace('ww.', '')

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
