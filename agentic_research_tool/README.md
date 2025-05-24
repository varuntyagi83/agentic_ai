# Agentic Research Tool

This Python script performs lightweight startup research by:
- Searching for the top 5 links using SerpAPI
- Scraping paragraphs from those pages
- Summarizing the key insights using OpenAI GPT-4

## Usage

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Create an `api_keys.json` file with the following format:
```json
{
  "OPENAI_API_KEY": "your-openai-key",
  "SERPAPI_KEY": "your-serpapi-key"
}
```

3. Run the script:
```
python main.py
```

## Output

Summarized key insights from top search results on the given startup or topic.
