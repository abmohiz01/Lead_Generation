from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")


def get_restaurant_info(search_query):

    try:
        # Construct the search URL
        base_url = "https://www.google.com/search?q="
        search_url = base_url + search_query.replace(" ", "+")

        # Navigate to the search URL
        driver.get(search_url)

        # Wait for the element to be clickable (adjust timeout as needed)
        element = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='Z4Cazf OSrXXb']")))

        # Click the element
        element.click()

        # Wait for the element with the information you want to retrieve (adjust timeout as needed)
        info_element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='dbg0pd' and @aria-level="3"]/span[@class='OSrXXb']"))
        )

        # Get text from the info element
        restaurant_info = info_element.text
        print("Restaurant Information:", restaurant_info)

    finally:
        # Close the browser window
        driver.quit()

# Example usage
search_query = "restaurants in west virginia"
get_restaurant_info(search_query)