from tools import openai_client
import io
import contextlib

def run_code():
    try:
        with open("generated_code.py", "r") as f:
            code = f.read()
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exec(code, {})
        output = buffer.getvalue()
        return f"✅ Code executed successfully:\n{output}" if output else "✅ Code executed successfully with no output."
    except Exception as e:
        return f"❌ Error during code execution: {e}"
