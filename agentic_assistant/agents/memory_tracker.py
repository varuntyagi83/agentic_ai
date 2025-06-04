
memory = []

def log(title, content):
    memory.append({ "title": title, "content": content })

def show_memory():
    for entry in memory:
        print(f"--- {entry['title']} ---")
        print(entry['content'])
        print("\n")

def clear_memory():
    memory.clear()
