
import os

# Global session state
state = {
    "task": "",
    "intent": "",
    "plan_complete": False,
    "code_written": False
}

def reset_state():
    state.update({
        "task": "",
        "intent": "",
        "plan_complete": False,
        "code_written": False
    })

def update_state(key, value=True):
    state[key] = value

def log_to_markdown(label, content):
    with open("agentic_output.md", "a") as f:
        f.write(f"\n\n=== {label} ===\n{content}\n")
    print("Saved session to agentic_output.md")
