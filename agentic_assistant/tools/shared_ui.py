from IPython.display import display, clear_output
import ipywidgets as widgets
from tools.session import update_state

def classify_intent(task: str) -> str:
    import openai
    glossary = (
        'travel: trip, itinerary, travel, vacation, holiday, journey, tourism, destination, sightseeing, backpacking\n'
        'research: report, summarize, explore, find, search, compare, analysis, benchmark, study\n'
        'code: code, function, script, automation, api, build, devops, program, generate, write'
    )
    prompt = (
        f"Based on the task below, classify its intent strictly as one of the following: travel, research, code.\n"
        f"Use the following glossary to decide intent:\n{glossary}\n\nTask: {task}"
    )
    response = openai.chat.completions.create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def render_main_ui():
    clear_output(wait=True)
    task_input = widgets.Text(
        placeholder="Describe your task here...",
        description="Prompt:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="80%")
    )
    detect_btn = widgets.Button(description="Detect Intent", button_style="info")

    def handle_submit(_):
        task = task_input.value.strip()
        if not task:
            print("⚠️ Please enter a task description.")
            return
        print("🔍 Detecting intent...")
        intent = classify_intent(task)
        update_state("intent", intent)
        print(f"🧠 Intent classified as: {intent}")
        if intent == "travel":
            from agents import travel_planner
            travel_planner.plan()
        elif intent == "research":
            from agents import research_planner
            research_planner.plan()
        elif intent == "code":
            from agents import code_task_planner
            code_task_planner.plan_code_task()
        else:
            print("❌ Unknown intent. Please try again.")

    detect_btn.on_click(handle_submit)
    display(task_input, detect_btn)