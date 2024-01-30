import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
import random

# List of proxies to rotate through
proxies = [
    '164.68.105.216:80',
    '134.209.29.120: 8080',
    '41.77.188.131:80',
    '195.23.57.78:80',
    '50.231.172.74:80'
    # Add more proxies as needed
]

# set options
options = Options()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

def get_random_proxy():
    return random.choice(proxies)

def set_proxy(proxy):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(options=chrome_options)

def find_relevant_info(results_container_element: WebElement) -> WebElement:
    return results_container_element.find_element(By.CLASS_NAME, "VkpGBb")

def get_company_info(url, name_to_type, proxy):
    try:
        # Initialize driver with proxy
        driver = set_proxy(proxy)

        # Navigate to the specified URL
        driver.get(url)
    except Exception as e:
        print("Error loading page")
        print(str(e))
        return None

    try:
        # Type the name into the text box
        text_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oc-header-search__input"))
        )
        text_box.send_keys(name_to_type)

        # Press Enter
        text_box.send_keys(Keys.RETURN)

        # Wait for the first link to be clickable
        first_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='company_search_result branch']"))
        )

        # Print the selected proxy
        print(f"Using Proxy: {proxy}")

        first_link.click()

        # Get agent name
        agent_name = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agent_name"))
        )

        # Get agent address
        agent_address = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agent_address"))
        )

        # Get original business name
        company_name = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wrapping_heading"))
        )
        Company = company_name.text.strip()

        # Get alternative name
        dd_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alternative_names"))
        )
        li_element = dd_element.find_element(By.CSS_SELECTOR, "ul.name_lines li.name_line")
        alternative_name = li_element.text.strip()

        return {
            "Alternative Name of business": alternative_name,
            "Agent Name": agent_name.text,
            "Agent Address": agent_address.text,
            "Original business name": Company
        }
    except Exception as e:
        print("Error during information retrieval")
        print(str(e))
        return None
    finally:
        # Close the WebDriver instance
        driver.quit()

def process_names(input_csv, output_csv, url, limit=30):
    with open(input_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        fieldnames = reader.fieldnames or []
        fieldnames += ["Alternative Name of business", "Agent Name", "Agent Address", "Original business name"]

        with open(output_csv, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for index, row in enumerate(reader):
                if index >= limit:
                    break

                name_to_type = row.get("name", "")

                # Get a random proxy for each iteration
                proxy = get_random_proxy()

                # Use the proxy in the get_company_info function
                result = get_company_info(url, name_to_type, proxy)

                if result:
                    row.update(result)
                    writer.writerow(row)

                    # Introduce a delay before the next iteration
                    time.sleep(10)  # Adjust the sleep duration as needed

# Example usage:
input_csv = "google_restaurants_list.csv"
output_csv = "output.csv"
url = 'https://opencorporates.com/companies/us_wv?q=&utf8=%E2%9C%93'

process_names(input_csv, output_csv, url, limit=30)