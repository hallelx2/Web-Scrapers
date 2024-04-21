import requests
from rich import print
import pandas as pd
import csv


def convert_to_indeed_jobs_csv(job_data, desired_columns=["title", "company", "location", "salaryInfo",'companyRating', "snippet", 'botUrl']):
  """
  Converts a list of dictionaries containing job information to a pandas DataFrame
  and exports it as a CSV file named "indeed_jobs.csv".

  Args:
      job_data: A list of dictionaries, where each dictionary represents a job listing.
      desired_columns: A list of strings specifying the desired columns to include in the CSV (default: ["title", "company", "location", "salaryInfo", "snippet"]).
  """

  # Extract relevant data and create a list of lists
  extracted_data = []
  for item in job_data:
    extracted_data.append([item.get(col) for col in desired_columns])

  # Create a pandas DataFrame
  df = pd.DataFrame(extracted_data, columns=desired_columns)

  # Export the DataFrame to a CSV file
  df.to_csv("indeed_jobs.csv", index=False)

  print("CSV file exported successfully!")
  
url = "https://www.simplyhired.com/_next/data/CrjGLb7NbUhm7ymGsRfbc/en-US/search.json"

querystring = {"q":"Dentist Jobs","l":""}

payload = ""
headers = {
    "cookie": "shk=1hrun7q4cmknh801; csrf=-nZ09ciM-NmGMfdhJjMbcXmlyNGObEJoxl5z0hI_zoJWHzEgYrYw7EST3JsywEFInWexZMscYablDZwFauZz; __cf_bm=yZqAokKpSg_UE4hbyGaZEGYKsidRE1pU4idbzIlEmqA-1713649216-1.0.1.1-KKSN_7PH1vCEBnFXOYt5GDq5WS4_JlXR58Ibo7Nl1K8E0ckY4Z8vpTpRTNN4SyVG1Ak1MCMJb2OU6JW6eLo5kA; _ga=GA1.1.1717221301.1713649238; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+20+2024+22%3A40%3A43+GMT%2B0100+(West+Africa+Standard+Time)&version=202308.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fcd3786b-e1cb-4730-9adc-99506412fad6&interactionCount=0&landingPath=https%3A%2F%2Fwww.simplyhired.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0007%3A0; rq=%5B%22q%3DDentist%2BJobs%26l%3DLagos%252C%2B05%26ts%3D1713649256308%22%5D; _ga_9GC5K2RCSP=GS1.1.1713649238.1.1.1713649257.0.0.0",
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-US;q=0.6",
    "priority": "u=1, i",
    "referer": "https://www.simplyhired.com/search?q=Dentist+Jobs&l=Lagos%2C+05",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring).json()

jobs = response['pageProps']['jobs']

convert_to_indeed_jobs_csv(jobs)



