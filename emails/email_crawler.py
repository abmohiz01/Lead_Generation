import re
from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class MailSpider(CrawlSpider):

    name = 'mails'
    start_urls = ['https://www.jerseymikes.com/26001/charles-town-wv']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'DEPTH_LIMIT': '2'

    }
    # Define rules for crawling
    def __init__(self, *args, **kwargs):
        super(MailSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]
    # Define rules for crawling
    rules = (
        Rule(LinkExtractor(allow=(r'/contact', r'/about')), follow=True, callback='parse_item'),
        Rule(LinkExtractor(deny_domains=(
            'facebook.com', 'google.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'twitter.com', 'apple.com')),
            follow=True,
            callback='parse_item'),
    )


    def parse_item(self, response):
        # Regex pattern for valid email addresses
        email_pattern = r'\w+@\w+\.(?:com|org|net|info|biz|us)'
        # Find all emails matching the pattern
        emails = re.findall(email_pattern, response.text)
        # Yield only the relevant emails
        for email in emails:
            if re.match(email_pattern, email):  # Check if the email matches the regex pattern
                yield {
                    'url': response.url,
                    'email': email
                }



