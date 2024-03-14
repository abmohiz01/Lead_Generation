
# Restaurant Lead Generation for Digital Marketing Agency

This project was designed to support a digital marketing agency by providing leads for restaurants in West Virginia. The primary focus was on extracting business emails from the restaurants' websites to facilitate the agency's pitching process.


## Features

- Utilized the Google Search API to extract data from 1907 restaurants.

- Post-processed the data to remove major chain restaurants like KFC, McDonald's, Subway, etc.

- Separated restaurants with Facebook links instead of websites.

- Developed a scrapy crawler to extract business emails from the restaurants' websites.

- Implemented a scraper for Facebook links to extract email and information from each Facebook link of restaurants.


## Get Started with Project

Clone the project

```bash
  git clone https://github.com/abmohiz01/Lead_Generation.git
```

Go to the project directory

```bash
  cd Lead_Generation(Restaurants)
```

Install the required dependencies by running:

```bash
  pip install -r requirements.txt
```


# Project_Structure

1. google_data_of_restaurants.py

- Run this file to extract the data from google search API.

- You can adjust the Region and County Coordinates according to your Requirements.

- Insert your API key from your GCP account to fetch the data with your request limit.

2. Filtering.py :
- This file allow to filter the websites of chain restaurants.

- Filtered domains.py file contains the restaurant names which are to be filtered.

3. 569_Filtered_URLS.json

- this will be  the generated JSON of the filtered restaurants data.

### Crawler :

1. Configure your scrapy environment.
- After Installing, Run :
```bash
scrapy startproject project_name 
```
to create a new Scrapy project.

2. Define a Spider, Use:
```bash 
scrapy genspider spider_name.
```
to create a new Spider

3. Run your Spider Using:  
```bash
scrapy crawl spider_name.
```
to run your Spider and start scraping.

4. To get the output of the crawler as an email, use the following command:

```bash
scrapy crawl spider_name -o filename.json
```
to run your Spider and start scraping

You Will get emails of each domain.

5. Run postprocessing.py to get the crawled emails of each domain.

### Facebook Scraper:

1. In Facebook_collections folder Run facebook_emails_scraper.py:

- It will get the filtered URLS containing facebook links instead of website.

- Navigate to each link by signing in your credentials and fetch the data for each profile.

- It will primarly focus on scraping the emails from the profiles.
