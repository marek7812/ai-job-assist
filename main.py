import requests
from bs4 import BeautifulSoup

def fetch_nofluff_jobs():
    print("Connecting to NoFluffJobs...")

    url = "https://nofluffjobs.com/pl/praca-zdalna?criteria=employment%3Dpermanent,zlecenie%20seniority%3Dtrainee,junior"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Successfully downloaded the page!\n")

        # Parser
        soup = BeautifulSoup(response.text, 'html.parser')

        job_links = []
        for a_tag in soup.find_all('a', href=True):
            if '/pl/job/' in a_tag['href']:
                job_links.append(a_tag['href'])

        unique_links = list(set(job_links))

        print(f"Found {len(unique_links)} job offers!\n")

        if unique_links:
            print("--- FOUND JOBS ---")
            for index, link in enumerate(unique_links, start=1):
                full_url = f"https://nofluffjobs.com{link}"
                print(f"{index}. {full_url}")
            print("------------------")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_nofluff_jobs()