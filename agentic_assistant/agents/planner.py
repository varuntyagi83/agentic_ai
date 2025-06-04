
import os
from agents import code_task_planner, travel_planner, research_planner
from openai import OpenAIError, OpenAI
from tools import openai_client


client = OpenAI()

def detect_intent(prompt):
    try:
        system_prompt = (
            "You are an intent classifier. "
            "Classify the user's request as one of: code, travel, research, website, or general. "
            "Respond with only the category name."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        intent = response.choices[0].message.content.strip().lower()
        print(f"🔍 LLM classified intent as: {intent}")
        return intent

    except (OpenAIError, ValueError, Exception) as e:
        print(f"⚠️ LLM-based intent detection failed: {e}")
        return fallback_intent(prompt)

def fallback_intent(prompt):
    prompt = prompt.lower()
    if any(keyword in prompt for keyword in ["travel", "trip", "vacation", "hotel", "flight"]):
        return "travel"
    elif any(keyword in prompt for keyword in ["research", "study", "review", "analyze", "paper"]):
        return "research"
    elif any(keyword in prompt for keyword in ["build", "code", "develop", "script", "program"]):
        return "code"
    else:
        return "general"

def plan(prompt):
    intent = detect_intent(prompt)
    if intent == "travel":
        return travel_planner.plan(prompt)
    elif intent == "research":
        return research_planner.plan(prompt)
    elif intent == "code":
        return code_task_planner.plan(prompt)
    else:
        print("🤖 Sorry, I couldn't determine the task type confidently. Please clarify if this is a code, travel, or research task.")
