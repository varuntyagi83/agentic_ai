
from openai import OpenAI
from tools import export_utils
from agents import memory_tracker
from tools import openai_client


client = OpenAI()

def write_code(prompt, language):
    try:
        task = f"Generate a complete, functional code solution in {language} for the following task:\n{prompt}"
        system_prompt = f"You are a senior {language} developer. Provide clean, production-grade code only."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task}
            ],
            temperature=0.3
        )
        code = response.choices[0].message.content.strip()

        # Save code to file
        with open("generated_code.py", "w") as f:
            f.write(code)

        memory_tracker.log("Generated Code", code)
        export_utils.save_to_markdown({
            "title": f"Generated {language} Code",
            "content": code,
            "followups": [
                "Would you like to run this code?",
                "Shall I write test cases for it?",
                "Want to deploy it as a microservice?"
            ]
        })
        return code

    except Exception as e:
        return f"❌ Code generation failed: {str(e)}"
