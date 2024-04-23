import requests
from requests_html import HTMLSession
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from rich import print

url = 'https://www.simplyhired.com/search?q=Dentist+Jobs&l='
base_url = 'https://www.simplyhired.com'

session = HTMLSession()
html = session.get(url)
content = html.text

soup = BeautifulSoup(content, 'html.parser')

job_cards = soup.find_all('div', class_ = 'css-f8dtpc')

def extract_job_details(job_card):
  """
  Extracts key features (title, company, location, salary, snippet, date, job URL) from a job listing HTML snippet.

  Args:
      html_content: The HTML content of the job listing snippet.

  Returns:
      A dictionary containing extracted key features of the job.
  """

 

    # Extract job title using data-testid
  job_title_element = soup.find('a', class_="chakra-button")
  job_title = job_title_element.text.strip() if job_title_element else None

  # Extract company name using data-testid
  company_element = soup.find('span', data_testid='companyName')
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
      'title': job_title,
      'company': company_name,
      'location': location,
      'salary': salary,
      'snippet': snippet,
      'date_posted': date_posted,
      'job_url': job_url
  }

  return job_details

overall = [extract_job_details(i) for i in job_cards]

df = pd.DataFrame(overall, columns=['TItle', 'Company', 'Location', 'Salary', 'Summary', 'Date Posted', 'Link'])

df.to_csv('simplyhired.csv', index=False)