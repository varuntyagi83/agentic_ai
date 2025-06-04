import ipywidgets as widgets
from tools.session import update_state
from agents import travel_planner, research_planner, code_task_planner
from tools.shared_ui import render_main_ui
import openai  # Keep this import at the top instead of inside the function

# Optional glossary for fast fallback routing
GLOSSARY = {
    "travel": [
        "vacation", "trip", "holiday", "flight", "hotel", "itinerary", 
        "travel", "roadtrip", "explore", "city tour", "weekend getaway"
    ],
    "research": [
        "research", "report", "compare", "market", "literature", 
        "topic", "review", "summary", "analyze", "insights"
    ],
    "code": [
        "code", "python", "sql", "generate", "script", "automation", 
        "docker", "fastapi", "data pipeline", "query", "build function"
    ]
}

# Hybrid intent classifier (safe, backward-compatible)
def classify_intent(task: str, safe_mode: bool = True) -> str:
    task_lower = task.lower()

    # Step 1: Try glossary first
    for intent, keywords in GLOSSARY.items():
        if any(keyword in task_lower for keyword in keywords):
            return intent

    # Step 2: GPT fallback
    if safe_mode:
        try:
            response = openai.chat.completions.create(
                model='gpt-4',
                messages=[{
                    'role': 'user',
                    'content': (
                        f"Classify the intent of this task: '{task}'. "
                        f"Choose from only: travel, research, or code. "
                        f"Only output the label — no explanation."
                    )
                }],
                temperature=0
            )
            result = response.choices[0].message.content.strip().lower()
            if result in {"travel", "research", "code"}:
                return result
        except Exception as e:
            print(f"Error during GPT classification: {e}")

    return "research"  # failsafe fallback

# Render the interface
render_main_ui()
