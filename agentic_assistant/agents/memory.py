class Memory:
    def __init__(self):
        self.history = []

    def log(self, label, content):
        self.history.append((label, content))
        print(f"[Memory] {label} logged.")