from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import csv

import time

from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

driver = webdriver.Chrome(options=options)

# Replace 'https://example.com' with the actual URL of the website you want to visit


def get_company_info(url, name_to_type):
    driver = webdriver.Chrome()

    try:
        # Navigate to the specified URL
        driver.get(url)

        # Type the name into the text box
        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oc-header-search__input"))
        )
        text_box.send_keys(name_to_type)

        # Press Enter
        text_box.send_keys(Keys.RETURN)

        # Wait for the first link to be clickable
        first_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='company_search_result branch']"))
        )
        first_link.click()

        # Optional: Wait for a few seconds to see the result (you may adjust the sleep time accordingly)
        time.sleep(10)

        # Get agent name
        agent_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agent_name"))
        )

        # Get agent address
        agent_address = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agent_address"))
        )

        # Get original business name
        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wrapping_heading"))
        )
        Company = company_name.text.strip()

        # Get alternative name
        dd_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alternative_names"))
        )
        li_element = dd_element.find_element(By.CSS_SELECTOR, "ul.name_lines li.name_line")
        alternative_name = li_element.text

        return {
            "Alternative Name of business": alternative_name,
            "Agent Name": agent_name.text,
            "Agent Address": agent_address.text,
            "Original business name": Company
        }

    except Exception as e:
        print(f"Error processing {name_to_type}: {str(e)}")
        return None

    finally:
        # Close the browser window
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
                result = get_company_info(url, name_to_type)

                if result:
                    row.update(result)
                    writer.writerow(row)

# Example usage:
input_csv = "google_restaurants_list.csv"  # Replace with your input CSV file path
output_csv = "output.csv"  # Replace with your desired output CSV file path
url = 'https://opencorporates.com/companies/us_wv?q=&utf8=%E2%9C%93'


process_names(input_csv, output_csv, url, limit=30)