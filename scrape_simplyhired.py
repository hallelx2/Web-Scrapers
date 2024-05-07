import pandas as pd
import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from rich import print
import datetime

base_url = "https://www.simplyhired.com"

# Function to Build the URL to search
def build_simplyhired_job_search_url(job_title, 
                                location, 
                                radius=None, 
                                fromage=None):
    """
    Builds a URL for searching jobs on Indeed with a specified job title, location, and optional radius.

    Args:
      job_title: The job title for the search (string).
      location: The desired location for the job search (city, state, or zip code).
      radius: The search radius in miles (optional, integer).

    Returns:
      A string containing the formatted Indeed job search URL.
    """
    # Indeed base URL for job search
    simplyhired_base_url = "https://www.simplyhired.com/search?"
    # Encode job title and location for safe URL inclusion
    encoded_job_title = urllib.parse.quote(job_title)
    encoded_location = urllib.parse.quote(location)

    # Build the URL with job title and location parameters
    search_url = simplyhired_base_url + f"q={encoded_job_title}&l={encoded_location}"

    # Add radius parameter if provided
    if radius:
        search_url += f"&sr={radius}"
    if fromage:
        search_url += f"&t={fromage}"
    return search_url

# List for the Things to be searched for
search_params = [
    'Dental Practices#Boston, MA# 100 miles',
    'Dental Practices#Houston, TX# 100 miles',
    'Dental Practices#Greensboro, NC# 50 miles',
    'Dental Practices#High point, NC# 50 miles', 
    'Dental Practices#Wintson-Salem, NC# 50 miles',
    'Dental Practices#Los Angeles, CA# 100 miles',
    'Dental Practices#Cleveland OH# 100 miles',
]

# To preprocess the search params for the inforamtion needed to build the link
# Not the best way but it is easy to modify
def preprocess_links(search_param):
    job, location, distance = search_param.split('#')
    dist= int(distance.strip().split(' ')[0])
    time = 7
    return (job, location, dist, time)

# The parsed links
parsed_output = [preprocess_links(search_param) for search_param in search_params]

links = []
for parsed in parsed_output:
    job, location, distance, fromage = parsed
    link = build_simplyhired_job_search_url(job, location, distance, fromage)
    links.append(link)


# Function to extract all the job links from the loaded page
def extract_job_details(job_card):
    """
    Extracts key features (title, company, location, salary, snippet, date, job URL) from a job listing HTML snippet.

    Args:
      html_content: The HTML content of the job listing snippet.

    Returns:
      A dictionary containing extracted key features of the job.
    """
    # Extract job title using data-testid
    job_title_element = job_card.find('h2', class_="chakra-text")
    job_title = job_title_element.find('a').text.strip() if job_title_element else None
    
    # Extract company name using data-testid
    company_element = soup.find('span', class_='css-lvyu5j')
    company_name = company_element.text.strip() if company_element else None


    # Extract location
    location_element = job_card.find('span', data_testid='searchSerpJobLocation')
    location = location_element.text.strip() if location_element else None

    # Extract salary
    salary_element = job_card.find('p', class_='chakra-text css-1g1y608')
    salary = salary_element.text.strip() if salary_element else None

    # Extract job snippet
    snippet_element = job_card.find('p', class_='chakra-text css-jhqp7z')
    snippet = snippet_element.text.strip() if snippet_element else None

    # Extract date posted
    date_element = job_card.find('p', class_='chakra-text css-5yilgw')
    date_posted = date_element.text.strip() if date_element else None

    # Extract job URL
    job_url_element = job_card.find('h2', class_='chakra-text css-8rdtm5').find('a')
    job_url = (base_url+job_url_element['href']) if job_url_element else None

    # Create a dictionary with extracted features
    job_details = {
      'Title': job_title,
      'Company': company_name,
      'Location': location,
      'Salary': salary,
      'Snippet': snippet,
      'Date Posted': date_posted,
      'Job Url': job_url
    }

    return job_details

# Set chrome to headless
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# Add the driver to be able to load the pages
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = chrome_options)

# Scrape the pages
job_list = []
for link in links:
    browser.get(link)
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')
    job_cards = soup.find_all('div', class_ = 'css-f8dtpc')
    job_list.extend([extract_job_details(job_card) for job_card in job_cards])

# Convert to a DataFrame
df = pd.DataFrame(job_list)

# Getting the current date and time to be able to name the csv file to be saved
current_datetime = datetime.datetime.now()
formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

#Save the dataframe to a CSV file
df.to_csv(f'scraped datasets/simplyhired {formatted_time}.csv', index=False)
print('Websites successfully scraped')