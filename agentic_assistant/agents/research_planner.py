
import ipywidgets as widgets
from IPython.display import display, clear_output
from tools import export_utils
from agents import memory_tracker
from openai import OpenAI
from tools import openai_client


client = OpenAI()

def generate_research_plan(topic, objective, source_type, output_format):
    try:
        prompt = (
            f"Prepare a complete research project plan based on the following inputs:\n"
            f"Topic: {topic}\n"
            f"Objective: {objective}\n"
            f"Preferred source type: {source_type}\n"
            f"Desired output format: {output_format}.\n"
            "The response should include:\n"
            "- A concise summary of the topic\n"
            "- A bullet outline of the research structure\n"
            "- Suggested sources or search terms for data\n"
            "- Tips for writing or formatting the output"
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant that returns structured research plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT failed to generate research plan: {str(e)}"

def plan(prompt):
    clear_output(wait=True)
    print("📚 Let's generate your research plan with GPT-4")

    topic = widgets.Text(description="Topic:")
    objective = widgets.Text(description="Objective:")
    source_type = widgets.Dropdown(
        options=["Academic", "Blogs", "Reports", "Mixed"],
        value="Mixed",
        description="Sources:"
    )
    output_format = widgets.RadioButtons(
        options=["Summary", "Presentation", "Paper", "Article"],
        description="Output:"
    )
    submit_button = widgets.Button(description="Generate Research Plan", button_style='success')

    abort_button = widgets.Button(description="Abort Task", button_style='danger')
    def abort_task(b):
        from IPython.display import Javascript
        display(Javascript('IPython.notebook.execute_cells([0])'))
    abort_button.on_click(abort_task)
    
    output = widgets.Output()

    def on_submit(b):
        with output:
            clear_output()
            plan = generate_research_plan(topic.value, objective.value, source_type.value, output_format.value)
            print(plan)
            memory_tracker.log("Research Plan", plan)
            export_utils.save_to_markdown({
                "title": f"Research Plan on {topic.value}",
                "content": plan,
                "followups": [
                    "Would you like me to gather sources now?",
                    "Shall I write the first section?",
                    "Want to turn this into a slide deck or draft document?"
                ]
            })

    submit_button.on_click(on_submit)
    display(widgets.VBox([topic, objective, source_type, output_format, abort_button, submit_button, output]))


def show_return_to_menu_buttons(current_plan_func):
    from IPython.display import display, clear_output
    import ipywidgets as widgets

    def start_new():
        from IPython.display import Javascript
        display(Javascript('IPython.notebook.execute_cells([0])'))

    def repeat_task(b):
        clear_output(wait=True)
        current_plan_func("")

    new_task_btn = widgets.Button(description="Start a New Task", button_style='info')
    repeat_btn = widgets.Button(description="Repeat This Task", button_style='primary')
    exit_btn = widgets.Button(description="Exit", button_style='danger')

    new_task_btn.on_click(lambda b: start_new())
    repeat_btn.on_click(repeat_task)
    exit_btn.on_click(lambda b: clear_output(wait=True))

    display(widgets.HBox([new_task_btn, repeat_btn, exit_btn]))

    show_return_to_menu_buttons(plan)