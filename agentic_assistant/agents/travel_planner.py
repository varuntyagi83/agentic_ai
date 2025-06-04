from IPython.display import display, clear_output, Markdown
import ipywidgets as widgets
from tools.session import log_to_markdown
from main_colab import render_main_ui
import openai
from tools import openai_client


def plan():
    clear_output(wait=True)
    display(Markdown("## 🌍 Let's plan your trip interactively and generate your itinerary!"))

    destination = widgets.Text(
        placeholder="e.g. Italy",
        description="Destination:",
        style={"description_width": "initial"}
    )

    dates = widgets.Text(
        placeholder="e.g. September 11 - September 15",
        description="Dates:",
        style={"description_width": "initial"}
    )

    budget = widgets.Dropdown(
        options=["Low", "Medium", "High"],
        value="Medium",
        description="Budget:",
        style={"description_width": "initial"}
    )

    interests = widgets.SelectMultiple(
        options=["Museums", "Nightlife", "Food", "Adventure", "Relaxation"],
        value=["Museums"],
        description="Interests:",
        style={"description_width": "initial"},
        layout=widgets.Layout(width="50%", height="120px")
    )

    gen_button = widgets.Button(description="Generate Itinerary", button_style="success")
    return_btn = widgets.Button(description="Return to Home", button_style="danger")

    display(destination, dates, budget, interests, widgets.HBox([gen_button, return_btn]))

    def on_generate(_):
        clear_output(wait=True)
        dest = destination.value
        date_range = dates.value
        money = budget.value
        prefs = list(interests.value)

        prompt = f"""You're a travel agent. Create a detailed itinerary for a trip to {dest} from {date_range}. 
        The traveler has a {money} budget and is interested in: {', '.join(prefs)}."""

        display(Markdown("### ✈️ Planning your trip..."))
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            itinerary = response.choices[0].message.content.strip()
            log_to_markdown("Travel Plan", itinerary)
            display(Markdown(itinerary))
        except Exception as e:
            display(Markdown(f"**Error:** {str(e)}"))

        
        return_home_btn = widgets.Button(description="Return to Home", button_style="info")
        def on_return(_):
            clear_output(wait=True)
            render_main_ui()
        return_home_btn.on_click(on_return)
        display(return_home_btn)
    

    def on_return(_):
        clear_output(wait=True)
        render_main_ui()

    gen_button.on_click(on_generate)
    return_btn.on_click(on_return)