# Import the necessary Libraries
from typing import Optional, Dict, Tuple
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from rich import print

# Add settings and Configurations
# Set chrome to headless
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Add the driver to be able to load the pages
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = chrome_options)

# Get the content of the website
website = 'https://ng.indeed.com/'
browser.get(website)

# Get the search area and button to be able to automate search
input_search = browser.find_element(By.ID, 'text-input-what')
search_button = browser.find_element(By.CLASS_NAME, 'yosegi-InlineWhatWhere-primaryButton')

# Automate the search process
input_search.clear()
input_search.send_keys('Dentist Jobs')
browser.execute_script("arguments[0].click();", search_button)

# Allow the page to load all its content fully before going to the other steps
sleep(5)


def get_data(job_listing):
    # Extract job title
    title = job_listing.find("a").find("span").text.strip()
    
    # Extract company name if available, otherwise assign an empty string
    try:
        company = job_listing.find('span', class_='css-92r8pb eu4oa1w0').text.strip()
    except AttributeError:
        company = ''
    
    # Extract job location if available, otherwise assign an empty string
    try:
        location  = job_listing.find('div', class_='css-1p0sjhy eu4oa1w0').text.strip()
    except AttributeError:
        location = ''
        
    # Extract salary information if available, otherwise assign an empty string
    try:
        salary  = job_listing.find('div', class_='metadata salary-snippet-container css-5zy3wz eu4oa1w0').text.strip()
    except AttributeError:
        salary = ''
    
    # Extract job type if available, otherwise assign an empty string
    try:
        job_type = job_listing.find('div', class_='metadata css-5zy3wz eu4oa1w0').text.strip()
    except AttributeError:
        job_type = ''
    
    # Extract date posted
    date_posted = job_listing.find('span', class_='css-qvloho eu4oa1w0').text.strip()
    
    # Extract job summary
    summary = job_listing.find('div', class_='css-9446fg eu4oa1w0').text.strip()
    
    # Return a tuple containing all the extracted information
    return (title, company, location, salary, job_type, date_posted, summary)

# Get the HTML source code of the page after it has fully loaded
html = browser.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# A list for all the job postings
job_listings = [get_data(i)for i in soup.find_all('div', class_='job_seen_beacon')]

# Convert list of records into a DataFrame
df = pd.DataFrame(job_listings, columns=['Title', 'Company', 'Location', 'Salary', 'Job Type', 'Date Posted', 'Summary'])
# Save DataFrame to a CSV file
df.to_csv('indeed_job_data.csv', index=False)

print("Data saved to job_data.csv")




