import json
from typing import Any
from urllib.parse import urlparse, urljoin
from collections import deque
from bs4 import BeautifulSoup
import requests
import re
import logging


# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebCrawler:
    def __init__(self, seed_url: str):
        self.seed_url = seed_url
        self.visited_urls = set()
        self.urls_to_visit = deque([seed_url])
        self.domain = self.get_domain(seed_url)

    @staticmethod
    def get_domain(url: str) -> str:
        return urlparse(url).netloc

    @staticmethod
    def is_valid_url(url: str) -> bool:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    @staticmethod
    def get_all_emails(soup: BeautifulSoup, domain: str) -> dict[str, list[Any]]:
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_pattern, soup.text)
        classified_emails = {"official": [], "other": []}
        for email in emails:
            email_domain = email.split('@')[-1]
            if email_domain == domain:
                classified_emails["official"].append(email)
            else:
                classified_emails["other"].append(email)
        return classified_emails

    @staticmethod
    def extract_filtered_urls(soup: BeautifulSoup, current_url: str, domain: str) -> list[str]:
        filtered_urls = []
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href and WebCrawler.is_valid_url(href):
                full_url = urljoin(current_url, href)
                if WebCrawler.get_domain(full_url) == domain and full_url != current_url:
                    filtered_urls.append(full_url)
        return filtered_urls

    def crawl(self) -> list[tuple[str, dict[str, list[Any]]]]:
        crawled_data = []
        logger.info(f"Starting crawl at {self.seed_url}")

        while self.urls_to_visit:
            current_url = self.urls_to_visit.popleft()
            logger.info(f"starting to crawl {current_url}")
            if current_url not in self.visited_urls:
                self.visited_urls.add(current_url)
                try:
                    response = requests.get(current_url, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(response.content, "html.parser")

                    urls = self.extract_filtered_urls(soup, current_url, self.domain)
                    for url in urls:
                        if url not in self.visited_urls and url not in self.urls_to_visit:
                            self.urls_to_visit.append(url)
                            logger.info(f"Added {url} to the queue.")

                    emails = self.get_all_emails(soup, self.domain)
                    crawled_data.append((current_url, emails))
                    logger.info(f"Crawled {current_url} and found emails: {emails}")
                except requests.RequestException as e:
                    logger.error(f"Error crawling {current_url}: {e}")

        logger.info("Finished crawling.")
        return crawled_data

    def convert_to_json(self, crawled_data: list[tuple[str, dict[str, list[Any]]]]) -> str:
        json_data = []
        for url, emails in crawled_data:
            json_data.append({
                "url": url,
                "emails": emails
            })
        return json.dumps(json_data, indent=2)

    def save_json_to_file(self, json_data: str, filename: str = "crawled_data.json"):
        with open(filename, "w") as json_file:
            json_file.write(json_data)


# Example usage
seed_url = "https://elkriverhotel.com/"
crawler = WebCrawler(seed_url)
data = crawler.crawl()
json_data = crawler.convert_to_json(data)
crawler.save_json_to_file(json_data)
