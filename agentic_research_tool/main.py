import os
import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Load API keys from file
def load_api_keys(filepath="api_keys.json"):
    if not os.path.exists(filepath):
        raise FileNotFoundError("Please provide a file named 'api_keys.json'")
    with open(filepath, "r") as f:
        keys = json.load(f)
        os.environ["OPENAI_API_KEY"] = keys.get("OPENAI_API_KEY", "")
        os.environ["SERPAPI_KEY"] = keys.get("SERPAPI_KEY", "")

# Perform search using SerpAPI
def search_startup(query):
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={SERPAPI_KEY}"
    res = requests.get(url)
    return [item['link'] for item in res.json().get('organic_results', [])[:5]]

# Extract main text content from URL
def extract_text(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        return ' '.join([p.get_text() for p in soup.find_all("p")])
    except Exception:
        return ""

# Summarize the extracted text using OpenAI
def summarize_content(text, company_name):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize the key info about {company_name} from this web content:\n\n{text[:5000]}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Main agentic research flow
def run_agentic_research(company):
    links = search_startup(company)
    summaries = []
    for url in links:
        text = extract_text(url)
        if text:
            summaries.append(summarize_content(text, company))
    return "\n\n".join(summaries)

if __name__ == "__main__":
    load_api_keys()
    print(run_agentic_research("Perplexity AI startup"))
