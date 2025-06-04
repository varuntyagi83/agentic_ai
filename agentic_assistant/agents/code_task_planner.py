from IPython.display import display, clear_output, Code, Markdown
import ipywidgets as widgets
from tools import openai_client
from tools.session import update_state, log_to_markdown, state
from agents import code_writer, test_writer, explainer
from tools.shared_ui import render_main_ui

def plan_code_task():
    clear_output(wait=True)
    display(Markdown("## 🧠 Let's plan your coding task step by step."))

    goal_input = widgets.Text(
        placeholder="e.g. Build a REST API to manage tasks",
        description="Goal:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="100%")
    )

    lang_dropdown = widgets.Dropdown(
        options=["Python", "JavaScript", "TypeScript", "SQL", "R", "Go", "Kotlin", "Java", "C++", "C#", "Bash", "Shell", "Rust", "Ruby", "PHP", "Swift", "Scala"],
        value="Python",
        description="Language:",
        style={"description_width": "initial"}
    )

    modules = widgets.SelectMultiple(
        options=["API", "Database", "UI", "Authentication", "Testing", "Deployment"],
        value=["API"],
        description="Modules:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="50%", height="120px")
    )

    include_tests = widgets.RadioButtons(
        options=["Yes", "No"],
        value="Yes",
        description="Include Tests?",
        style={"description_width": "initial"}
    )

    plan_btn = widgets.Button(description="Generate Code Plan", button_style="success")
    abort_btn = widgets.Button(description="Abort Task", button_style="danger")
    display(goal_input, lang_dropdown, modules, include_tests, widgets.HBox([abort_btn, plan_btn]))

    def on_abort(_):
        clear_output(wait=True)
        render_main_ui()

    def on_generate(_):
        clear_output(wait=True)
        goal = goal_input.value.strip()
        language = lang_dropdown.value
        selected_modules = list(modules.value)
        want_tests = include_tests.value == "Yes"

        summary = f"Goal: {goal}\nLanguage: {language}\nModules: {', '.join(selected_modules)}\nInclude Tests: {want_tests}"
        log_to_markdown("Code Plan", summary)
        update_state("goal", goal)
        update_state("language", language)
        update_state("modules", selected_modules)
        update_state("include_tests", want_tests)
        update_state("plan_complete", True)

        display(Markdown("### ✅ Code plan created! Now you can write, test or explain your code."))

        write_btn = widgets.Button(description="Write Code", button_style="primary")
        return_btn = widgets.Button(description="Return to Home", button_style="info")
        display(widgets.HBox([write_btn, return_btn]))

        def on_return(_):
            clear_output(wait=True)
            render_main_ui()

        def on_write(_):
            clear_output(wait=True)
            display(Markdown("### 💻 Writing code based on your plan..."))
            code = code_writer.write_code(goal, language)
            state["last_code"] = code
            display(Code(code, language=language.lower()))

            test_btn = widgets.Button(description="Test Code", button_style="success")
            explain_btn = widgets.Button(description="Explain Code", button_style="warning")
            return_btn2 = widgets.Button(description="Return to Home", button_style="info")
            display(widgets.HBox([test_btn, explain_btn, return_btn2]))

            def on_test(_):
                clear_output(wait=True)
                display(Markdown("### 🧪 Testing code..."))
                test_writer.run_tests()

                explain_btn2 = widgets.Button(description="Explain Code", button_style="warning")
                return_btn3 = widgets.Button(description="Return to Home", button_style="info")
                explain_btn2.on_click(lambda _: [clear_output(wait=True), explainer.explain(code), display(return_btn3)])
                return_btn3.on_click(lambda _: render_main_ui())
                display(widgets.HBox([explain_btn2, return_btn3]))

            def on_explain(_):
                clear_output(wait=True)
                explainer.explain(code)
                return_btn4 = widgets.Button(description="Return to Home", button_style="info")
                return_btn4.on_click(lambda _: render_main_ui())
                display(return_btn4)

            test_btn.on_click(on_test)
            explain_btn.on_click(on_explain)
            return_btn2.on_click(lambda _: render_main_ui())

        write_btn.on_click(on_write)
        return_btn.on_click(on_return)

    plan_btn.on_click(on_generate)
    abort_btn.on_click(on_abort)
