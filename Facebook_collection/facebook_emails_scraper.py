import json
import re
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By


def convert_to_web_facebook(url):
    # This regex pattern matches the mobile Facebook domain and captures the rest of the URL
    pattern = r"https?://m\.facebook\.com(/.*)"
    replacement = r"https://www.facebook.com\1"  # Replace with the web domain, keeping the rest of the URL

    # Replace the domain using re.sub
    web_url = re.sub(pattern, replacement, url)
    return web_url


options = webdriver.ChromeOptions()
options.add_argument('User-Agent: Mozilla/5.0')
driver = webdriver.Chrome(options=options)

with open('google_restaurants_list.json', 'r') as f:
    google_restaurants = json.load(f)

facebook_domains = []
for restaurant in google_restaurants:
    domain = urllib.parse.urlparse(restaurant['website']).netloc if restaurant.get('website') else None
    if domain and 'facebook' in domain:
        facebook_domains.append(restaurant)

with open('facebook_restaurants.json', 'w') as f:
    json.dump(facebook_domains, f)

driver.get('https://www.facebook.com')
driver.find_element(By.ID, 'email').send_keys('$$$$$$$$$$$$@gmail.com')
driver.find_element(By.ID, 'pass').send_keys('$$$$$$$$$$')
driver.find_element(By.XPATH,
                    '/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button').click()
time.sleep(10)

for restaurant in facebook_domains:
    restaurant['website'] = convert_to_web_facebook(restaurant['website'])
    driver.get(restaurant['website'])
    if 'Page not found' in driver.title:
        print('Facebook page not found for business: ', restaurant['name'])
        continue
    email_pattern = r'\w+@\w+\.(?:com|org|net|info|biz|us)'
    emails = re.findall(email_pattern, driver.page_source)
    if emails:
        print('Emails found on facebook page for business: ', restaurant['name'])
        print(emails)
        restaurant['emails'] = emails
    else:
        print('No emails found on facebook page for business: ', restaurant['name'])

with open('facebook_restaurants_with_emails.json', 'w') as f:
    json.dump(facebook_domains, f)
driver.quit()