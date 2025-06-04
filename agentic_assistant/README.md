
# 🧠 Agentic Assistant

**Modular GPT-powered AI Agent System for Task Automation in Google Colab**

This project demonstrates how to build and deploy autonomous AI agents for different types of knowledge work — including travel planning, code generation, and research assistance — all within a unified, extensible system.

---

## 🚀 Features

- 🔍 **Intent Classification** — Automatically routes user prompts to the correct agent
- 🧭 **Travel Planner** — Generates multi-day itineraries based on destination, dates, budget, and interests
- 🧑‍💻 **Code Task Planner** — Writes, tests, and explains code in multiple languages
- 📚 **Research Planner** — Summarizes articles, papers, or market research
- ✅ **Step-by-Step Workflow UI** — With widgets for input, output, explanations, and export
- 🔐 **Secure OpenAI Key Management** using `.env` and `python-dotenv`

---

## 📦 Folder Structure

```
agentic_assistant/
├── agents/
│   ├── travel_planner.py
│   ├── code_task_planner.py
│   ├── research_planner.py
│   └── ...
├── tools/
│   ├── openai_client.py         # ✅ Loads key from .env securely
│   ├── session.py
│   ├── shared_ui.py
│   └── ...
├── main_colab.py                # 👇 Main entry point for running in Colab
├── requirements.txt
└── README.md
```

---

## 🧑‍💻 How to Run in Google Colab

### Step 1: Upload the ZIP to Colab
```python
from google.colab import files
uploaded = files.upload()  # Upload `agentic_assistant.zip`
```

### Step 2: Unzip
```python
import zipfile
with zipfile.ZipFile("agentic_assistant.zip", "r") as zip_ref:
    zip_ref.extractall(".")
%cd agentic_assistant
```

### Step 3: Install Dependencies
```python
!pip install -r requirements.txt
```

### Step 4: Create a `.env` File for Your OpenAI Key
```python
with open(".env", "w") as f:
    f.write("OPENAI_API_KEY=sk-...")  # Replace with your key
```

### Step 5: Run the Interface
```python
%run main_colab.py
```

---

## 🛡️ Security

All OpenAI key usage is managed centrally via:
```python
tools/openai_client.py
```
This file loads your key using:
```python
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
```

---

## 📈 Extend the Agent System

Add a new agent:
1. Create a file: `agents/finance_planner.py`
2. Import and register it in `main_colab.py`
3. Extend the `classify_intent()` function with new keywords
4. Build UI using widgets

---

## ✍️ Author

Built by [Your Name] — Inspired by task overload and the need for smart, focused digital teammates.

---

## 📜 License

MIT License
