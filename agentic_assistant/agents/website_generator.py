
def generate_website():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>My AI-Generated Site</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; color: #333; }
        h1 { color: #0056b3; }
        p { font-size: 18px; }
    </style>
</head>
<body>
    <h1>Welcome to Your AI-Generated Website!</h1>
    <p>This static website was created using your DevOps Copilot agent.</p>
</body>
</html>
"""
    with open("website.html", "w") as f:
        f.write(html_content)
    print("Website generated as 'website.html'")
