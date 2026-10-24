import time
import requests
from bs4 import BeautifulSoup

def load_prompt():
    try:
        with open("prompt.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "[ERROR] prompt.txt not found. Please create one based on the documentation."

def get_job_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        main_content = soup.find("main")

        if main_content:
            text = main_content.get_text(separator="\n", strip=True)
        else:
            text = soup.body.get_text(separator="\n", strip=True)

        # Filter out the trash categories
        cutoff_markers = [
            "Zobacz podobne oferty",
            "Sprawdź zarobki",
            "O firmie",
            "Oceń tę ofertę",
        ]
        for marker in cutoff_markers:
            if marker in text:
                text = text.split(marker)[0]

        return text.strip()
    return None


def analyze_job(job_description):
    # KoboldCPP + qwen2.5-7b-instruct-q6_k
    url = "http://localhost:5001/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    prompt = load_prompt()

    if "[ERROR]" in prompt:
        return prompt

    payload = {
        "messages": [
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": f"Please analyze this job description:\n{job_description}",
            },
        ],
        "temperature": 0.1,
        "max_tokens": 80,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Error while connecting with LLM: {e}"


def fetch_nofluff_jobs():
    print("Connecting to NoFluffJobs...")
    url = "https://nofluffjobs.com/pl/praca-zdalna?criteria=employment%3Dpermanent,zlecenie%20seniority%3Dtrainee,junior"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Page download successfull!\n")

        soup = BeautifulSoup(response.text, "html.parser")
        job_links = []
        for a_tag in soup.find_all("a", href=True):
            if "/pl/job/" in a_tag["href"]:
                job_links.append(a_tag["href"])

        unique_links = list(set(job_links))
        print(f"Found {len(unique_links)} job offers!\n")

        if unique_links:
            print("--- FETCHING DETAILS AND ANALYZING ---")

            for index, link in enumerate(unique_links, start=1):
                full_url = f"https://nofluffjobs.com{link}"
                print(f"\n[{index}] Scraping: {full_url}")

                job_text = get_job_details(full_url)

                if job_text:
                    print(f"Done! ({len(job_text)} chars) Sending to Qwen...")
                    ai_response = analyze_job(job_text)
                    print("\n--- Response ---")
                    print(ai_response)
                    print("------------------")
                else:
                    print("Failed to extract details.")

                time.sleep(6)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


if __name__ == "__main__":
    fetch_nofluff_jobs()