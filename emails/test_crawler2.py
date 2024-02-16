import re
from urllib.parse import urlparse
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json

# Assuming urls_to_crawl.json is correctly formatted and accessible
with open('urls_to_crawl.json', 'r') as file:
    urls = json.load(file)

urls_to_scrape = list(urls.values())[:20]
print(len(urls_to_scrape))


class MailSpider(CrawlSpider):
    name = 'mails'
    start_urls = urls_to_scrape
    allowed_domains = [urlparse(url).netloc for url in urls_to_scrape]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'DEPTH_LIMIT': '2',
        'ROBOTSTXT_OBEY' : 'False',
        'CONCURRENT_REQUESTS' : '32',
        'DOWNLOAD_DELAY' : '0.25'
    }

    def __init__(self, *args, **kwargs):
        super(MailSpider, self).__init__(*args, **kwargs)
        self.scraped_items_count = {}
        self.scraped_emails = {}

    rules = (
        Rule(LinkExtractor(allow=(r'/contact', r'/about')), follow=True, callback='parse_item'),
        Rule(LinkExtractor(deny_domains=(
            'facebook.com', 'google.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'twitter.com', 'apple.com')),
            follow=True,
            callback='parse_item'),
    )

    def parse_item(self, response):
        domain = urlparse(response.url).netloc
        if domain not in self.scraped_items_count:
            self.scraped_items_count[domain] = 0
            self.scraped_emails[domain] = set()

        if self.scraped_items_count[domain] >= 10:
            return

        email_pattern = r'\w+@\w+\.(?:com|org|net|info|biz|us)'
        emails = re.findall(email_pattern, response.text)

        for email in emails:
            if email not in self.scraped_emails[domain]:
                self.scraped_emails[domain].add(email)
                self.scraped_items_count[domain] += 1
                yield {
                    'url': response.url,
                    'email': email
                }

                if self.scraped_items_count[domain] >= 10:
                    break