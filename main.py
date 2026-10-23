import requests
import time
from bs4 import BeautifulSoup

def get_job_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('main')

        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
            return text
        else:
            return soup.body.get_text(separator='\n', strip=True)
    return None

def fetch_nofluff_jobs():
    print("Connecting to NoFluffJobs...")
    url = "https://nofluffjobs.com/pl/praca-zdalna?criteria=employment%3Dpermanent,zlecenie%20seniority%3Dtrainee,junior"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Page download successfull!\n")

        soup = BeautifulSoup(response.text, 'html.parser')
        job_links = []
        for a_tag in soup.find_all('a', href=True):
            if '/pl/job/' in a_tag['href']:
                job_links.append(a_tag['href'])

        unique_links = list(set(job_links))
        print(f"Found {len(unique_links)} job offers!\n")

        if unique_links:
            print("--- FETCHING DETAILS ---")

            #Testing if I get ratelimit
            for index, link in enumerate(unique_links[:len(unique_links)], start=1):
                full_url = f"https://nofluffjobs.com{link}"
                print(f"\n[{index}] Scraping: {full_url}")

                job_text = get_job_details(full_url)

                if job_text:
                    print(f"Great! Extracted {len(job_text)} characters.")
                    preview = job_text[:150].replace('\n', ' ')
                    print(f"Preview: {preview}...")
                else:
                    print("Failed to extract details.")

                time.sleep(5)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_nofluff_jobs()