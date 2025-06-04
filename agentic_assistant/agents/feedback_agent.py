
from agents import test_writer, explainer, planner
from tools import openai_client


def ask_followup():
    options = [
        "Do you want to test the code?",
        "Do you want to generate a website from this?",
        "Would you like me to explain what I just wrote?",
        "Do you have another task for me?"
    ]
    print("\nWhat would you like to do next?")
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")

    choice = input("Enter number: ")
    if choice == "1":
        test_writer.run_tests()
    elif choice == "2":
        planner.plan_website_task()
    elif choice == "3":
        explainer.explain()
    elif choice == "4":
        planner.get_new_task()
    else:
        print("Invalid choice or exiting. Thank you!")
