from agents.planner import plan
from agents.code_writer import write_code
from agents.test_writer import write_tests
from agents.runner import run_tests, run_script
from agents.explainer import explain
from agents.memory import Memory

def run_agent():
    memory = Memory()
    prompt = input("Enter your task: ")
    language = input("Which programming language do you want the code in? (e.g., Python, JavaScript, SQL): ").strip()

    memory.log("Prompt", prompt)
    memory.log("Language", language)
    steps = plan(prompt)
    print(f"Plan: {steps}")

    code = write_code(prompt, language)
    memory.log("Generated Code", code)

    if language.lower() == "python":
        tests = write_tests(code)
        memory.log("Generated Tests", tests)

        passed, test_output = run_tests(code, tests)
        memory.log("Test Output", test_output)

        if not passed:
            print("Tests failed. Attempting to explain and stop.")
            explanation = explain(test_output)
            print("Explanation:", explanation)
        else:
            print("Tests passed. Running script...")
            result = run_script(code)
            print("Result:", result)
    else:
        print(f"Code generation for {language} completed.")
        print(code)

from agents import feedback_agent

feedback_agent.ask_followup()


def run_pipeline(prompt):
    from agents import planner, code_writer
    print("Planning task...")
    planner.plan(prompt)
    print("Writing code...")
    code_writer.write_code(prompt)
    from agents import feedback_agent
    feedback_agent.ask_followup()
