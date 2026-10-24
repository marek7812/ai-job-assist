# Job Scraper & AI Evaluator

This is an automatic Python tool that collects job ads from certain websites and serves as a job search assistant. It compares each ad to a defined candidate profile and selects the most appropriate resume based on the job posting through the use of local LLM.

## How It Works

**Web Scraping:** Fetches job postings for selected roles directly from desired website.

**Noise Reduction:** Cleans up the scraped data by removing salary sliders, recommended offers etc.

**Evaluation:** Sends the cleaned job description to a local LLM instance running via KoboldCPP.

**Strict Decision Logic:** Evaluates hard requirements (e.g., rejecting non-matching languages, senior roles, or non-IT positions) and suggests the exact tailored CV file to use (e.g., technical vs. support, Polish vs. English).

## Quickstart

### Prerequisites

- Python 3.10+
- Local AI Engine (For example) [KoboldCPP](https://github.com/LostRuins/koboldcpp)
- LLM Model (Recommended) `qwen2.5-7b-instruct-q6_k.gguf` (or a similar 7B-class instruct model)
- Hardware: GPU with Vulkan or CUDA support

### 1. Install dependencies

```
pip install -r requirements.txt

```

### 2. Configure candidate profile
Create a file named prompt.txt in the main directory. This file should contain the system prompt with your specific profile, tech stack and evaluation rules.

### 3. Start the local LLM server

Place `.gguf` model in your working directory and start KoboldCPP. Adjust `--contextsize` and `--gpulayers` based on your hardware:

```
koboldcpp.exe --usevulkan --gpulayers 99 --contextsize 3072 --highpriority --model qwen2.5-7b-instruct-q6_k.gguf

```

### 4. Run the evaluator

Ensure the local server is running on `http://localhost:5001`, then run the script:

```
python main.py

```

## Expected Output

The script outputs the scraped link, the LLM's brief Chain of Thought and the final decision:

```
[1] Scraping: https://nofluffjobs.com/pl/job/...
Done! (4355 chars) Sending to Qwen...

--- Response ---
Analysis: The role is in Sales and requires B2 level of English and Polish, which the candidate meets. However, the role is not IT-related and does not fit the candidate's technical background.
Decision: Do not apply
------------------
```
