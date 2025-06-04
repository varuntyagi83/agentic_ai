from tools.openai_client import chat
from IPython.display import display, Markdown
from tools import openai_client


def explain(code):
    if not code:
        display(Markdown("⚠️ **No code provided to explain.**"))
        return

    prompt = f"Explain what this code does in simple terms:\n\n```python\n{code}\n```"
    explanation = chat(prompt)
    display(Markdown(f"### 🧠 Code Explanation:\n\n{explanation}"))