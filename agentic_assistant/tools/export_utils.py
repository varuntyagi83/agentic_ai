
import os

EXPORT_FILE = "agentic_output.md"
memory_log = []

def save_to_markdown(entry, intent="general"):
    memory_log.append(entry)
    with open(EXPORT_FILE, "w") as f:
        f.write(f"# Agentic Assistant Session\n\n")
        for item in memory_log:
            f.write(f"## {item['title']}\n\n")
            f.write(f"{item['content']}\n\n")
            if 'followups' in item:
                f.write("**Suggested Next Steps:**\n")
                for tip in item['followups']:
                    f.write(f"- {tip}\n")
            f.write("\n---\n")

    print(f"Saved session to {EXPORT_FILE}")
