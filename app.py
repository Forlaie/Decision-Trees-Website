from shiny import reactive, render
from shiny.express import input, ui
from functools import partial
from shiny.ui import page_navbar
import plotly.graph_objects as go
from shinywidgets import render_plotly

import math
def calculate_entropy(n1, n2, t):
    p1 = n1/t
    p2 = n2/t
    log1 = 0 if p1 == 0 else math.log2(p1)
    log2 = 0 if p2 == 0 else math.log2(p2)

    return 0.0 if round(-p1 * log1 - p2 * log2, 2) == 0.0 else round(-p1 * log1 - p2 * log2, 2)

def calculate_condent(n1, n2, t, e1, e2):
    p1 = n1/t
    p2 = n2/t
    return round(p1 * e1 + p2 * e2, 2)

def calculate_infogain(e1, e2):
    return round(e1-e2, 2)

def create_mathjax_content(info):
    # Base MathJax content
    lines = {
        1: f"""
            \\[H(Y) = -\\frac{info['lemons']}{info['total']}log_{2}\\frac{info['lemons']}{info['total']} -\\frac{info['oranges']}{info['total']}log_{2}\\frac{info['oranges']}{info['total']}\\approx{info['h_y']}\\]
        """,
        2: f"""
            \\[H(Y|{info['side1']}) = -\\frac{info['side1_lemon']}{info['side1s']}log_{2}\\frac{info['side1_lemon']}{info['side1s']} -\\frac{info['side1_orange']}{info['side1s']}log_{2}\\frac{info['side1_orange']}{info['side1s']}\\approx{info['h_yside1']}\\]
        """,
        3: f"""
            \\[H(Y|{info['side2']}) = -\\frac{info['side2_lemon']}{info['side2s']}log_{2}\\frac{info['side2_lemon']}{info['side2s']} -\\frac{info['side2_orange']}{info['side2s']}log_{2}\\frac{info['side2_orange']}{info['side2s']}\\approx{info['h_yside2']}\\]
        """,
        4: f"""
            \\[H(Y|X) = \\frac{info['side1s']}{info['total']}\\cdot{info['h_yside1']} + \\frac{info['side2s']}{info['total']}\\cdot{info['h_yside2']}\\approx{info['h_yx']}\\]
        """,
        5: f"""
            \\[IG(Y|X) = {info['h_y']} - {info['h_yx']} \\approx {info['infogain']}\\]
        """
    }
    
    # Start the HTML content
    mathjax_html = """
    <script type="text/javascript" async 
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>

    <div style="text-align: top; font-size: 17px; font-weight: normal; color: #1F4A89; line-height: 1;">
    """
    
    # Add the selected line based on the `step`
    for i in range(1, 5):
        if i <= step.get():
            mathjax_html += lines[i]

    # Close the div and script tags
    mathjax_html += """
    </div>

    <script type="text/javascript">
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    </script>
    """
    
    return mathjax_html


# Starter datapoints to plot
o_points = reactive.value({'x': [1, 1, 5, 8, 8], 'y': [3, 7, 7, 4, 7]})
l_points = reactive.value({'x': [5, 8], 'y': [4, 3]})
x_coord = reactive.value(0)
y_coord = reactive.value(0)
vertical_split = reactive.value(True)
split_loc = reactive.value(3)
notation = reactive.value(False)
variables = reactive.value(False)
definition = reactive.value(False)
step = reactive.value(0)

# Make main screen, with title and page navigation
ui.page_opts(
    title="Decision Trees",  
    page_fn=partial(page_navbar, id="page"),
    fillable=True,
)

def make_normal_text(text):
    return ui.tags.span(ui.HTML(f"""
            <span style="font-size: 17px; font-weight: normal; color: #1F4A89; line-height: 1; vertical-align: middle;">
                \\({text}\\)
            </span>
        """))

with ui.nav_panel("Test"):
    with ui.tags.div(style="text-align: center;"):

        # Tooltip only for H(Y) = -
        with ui.tooltip(id="btn_tooltip", placement="right"):  
            ui.tags.span(ui.HTML(f"""
                                <script type="text/javascript" async 
                                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
                                </script>
                                <span style="text-align: center; font-size: 17px; font-weight: normal; color: #1F4A89; line-height: 1;">
                                    \\(H(Y)\\)
                                </span>
                                    
                                
                            """))
            ui.HTML(f"""
                    <script type="text/javascript" async 
                        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
                    </script>
                    \\(Y \\in \\lbrace oranges, lemons \\rbrace \\)""")  # Tooltip content

        # "test" placed outside the tooltip but still inline
        make_normal_text("= -")

#H(Y) = -\\frac{lemons}{total}log_{2}\\frac{lemons}{total} -\\frac{oranges}{total}log_{2}\\frac{oranges}{total}\\approx{h_y}\\

    @render.text
    def btn_tooltip_state():
        return f"Tooltip state: {input.btn_tooltip()}"


# Information gain page
with ui.nav_panel("Information Gain"):

    # Put cards in a column
    with ui.layout_columns():
        # Features card
        with ui.card():
            ui.card_header("Features", style="font-size: 20px;")
            
            # Sidebar for coordinate selection
            with ui.layout_sidebar():
                with ui.sidebar(open="closed", bg="#f8f8f8", width="300px"):
                    "Datapoint Coordinate Selection"
                    ui.input_slider("xcoord", "X-coord", 0, 10, 0),
                    @reactive.effect
                    @reactive.event(input.xcoord)
                    def xvalue():
                        x_coord.set(input.xcoord())
                    
                    ui.input_numeric("ycoord", "Y-coord", 1, min=1, max=10),
                    
                    @reactive.effect
                    @reactive.event(input.ycoord)
                    def yvalue():
                        y_coord.set(input.ycoord())
                    
                    @render.text()
                    def error_check():
                        if not isinstance(input.ycoord(), int):
                            return "Invalid coordinate"
            
            with ui.layout_columns():
                ui.input_switch("vertical", "Vertical Split", True)  
                @reactive.effect
                @reactive.event(input.vertical)
                def change_split_direction():
                    vertical_split.set(input.vertical())
                
                ui.input_slider("split_loc", "Split Location", 0, 10, 3),
                @reactive.effect
                @reactive.event(input.split_loc)
                def change_split_location():
                    split_loc.set(input.split_loc())

            # Plot where students will be putting datapoints and split
            @render_plotly
            def feature_plot():
                fig = go.Figure()
                # Add orange points (circles)
                fig.add_trace(go.Scatter(
                    x=o_points.get()['x'],
                    y=o_points.get()['y'],
                    mode='markers',
                    name='Orange',
                    marker=dict(
                        color='red',
                        size=12,
                        symbol='circle',
                        line=dict(
                            color=['black', 'black', 'black', 'white', 'black'],  # Outline for some points
                            width=[2, 0, 2, 0, 2]  # 0 width removes outline for some points
                        )
                    )
                ))
                fig.add_trace(go.Scatter(
                    x=l_points.get()['x'],
                    y=l_points.get()['y'],
                    mode='markers',
                    name='Lemon',
                    marker=dict(
                        color='blue',
                        size=12,
                        symbol='triangle-up'
                    )
                ))
                fig.update_layout(
                    xaxis=dict(range=[0, 10]),
                    yaxis=dict(range=[0, 10]),
                    xaxis_title="Width",
                    yaxis_title="Height",
                    showlegend=True,
                    plot_bgcolor='white',
                    xaxis_showgrid=True,
                    yaxis_showgrid=True,
                    xaxis_gridcolor='rgba(0, 0, 0, 0.1)',
                    yaxis_gridcolor='rgba(0, 0, 0, 0.1)',
                    xaxis_gridwidth=1,
                    yaxis_gridwidth=1
                )
                # split location
                if (vertical_split.get()):
                    fig.add_vline(x=split_loc.get(), line=dict(color="purple", width=2, dash="dash"), name="Vertical Line")
                else:
                    fig.add_hline(y=split_loc.get(), line=dict(color="purple", width=2, dash="dash"), name="Horizontal Line")
                return fig
            
            # Buttons to add datapoints
            with ui.layout_columns():
                ui.input_action_button("add_orange_button", "Add orange datapoint", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
                ui.input_action_button("add_lemon_button", "Add lemon datapoint", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
            
            # Add a new orange datapoint button
            @reactive.effect
            @reactive.event(input.add_orange_button)
            def add_orange():
                curr_points = o_points.get()
                updated_points = {
                    'x': curr_points['x'] + [x_coord.get()],
                    'y': curr_points['y'] + [y_coord.get()],
                }
                o_points.set(updated_points)
            
            # Add a new lemon datapoint button
            @reactive.effect
            @reactive.event(input.add_lemon_button)
            def add_lemon():
                curr_points = l_points.get()
                updated_points = {
                    'x': curr_points['x'] + [x_coord.get()],
                    'y': curr_points['y'] + [y_coord.get()],
                }
                l_points.set(updated_points)
            
            # Buttons to remove datapoints
            with ui.layout_columns():
                ui.input_action_button("remove_orange_button", "Remove orange datapoint", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
                ui.input_action_button("remove_lemon_button", "Remove lemon datapoint", style="color: #fff; background-color: #337ab7; border-color: #2e6da4")

            # Remove an orange datapoint button
            @reactive.effect
            @reactive.event(input.remove_orange_button)
            def remove_orange():
                curr_points = o_points.get()
                if len(curr_points['x']) > 0:
                    curr_points['x'].pop()
                    curr_points['y'].pop()
                    updated_points = {
                        'x': curr_points['x'],
                        'y': curr_points['y'],
                    }
                    o_points.set(updated_points)
            
            # Remove a lemon datapoint button
            @reactive.effect
            @reactive.event(input.remove_lemon_button)
            def remove_lemon():
                curr_points = l_points.get()
                if len(curr_points['x']) > 0:
                    curr_points['x'].pop()
                    curr_points['y'].pop()
                    updated_points = {
                        'x': curr_points['x'],
                        'y': curr_points['y'],
                    }
                    l_points.set(updated_points)

        # Calculations card
        with ui.card():
            ui.card_header("Calculations", style="font-size: 20px;")
            @render.ui()
            def show_stuff():
                if notation.get():
                    return ui.p(
                        ui.HTML("""
                            <div style="text-align: center; font-size: 24px; font-weight: normal; color: #9370DB;">
                                <span style="font-weight: bold; color: #1F4A89;">Equation:</span> 
                                IG(<span style="color: #1F4A89;">Y</span>|<span style="color: #1F4A89;">X</span>) 
                                <span style="color: #1F4A89;">=</span> 
                                H(<span style="color: #1F4A89;">Y</span>) 
                                <span style="color: #1F4A89;">-</span> 
                                H(<span style="color: #1F4A89;">Y</span>|<span style="color: #1F4A89;">X</span>)
                            </div>
                            
                            <div style="display: flex; justify-content: center; gap: 20px;">
                                <div style="position: relative; text-align: center; margin-left: 150px;">
                                    <span style="font-size: 18px; color: #9370DB;">Information gain</span>
                                    <div style="
                                        position: absolute;
                                        top: -35px;
                                        left: 55%;
                                        transform: translateX(-50%) rotate(35deg);
                                        font-size: 30px;
                                        color: #9370DB;">
                                        &uarr;
                                    </div>
                                </div>
                                
                                <div style="position: relative; text-align: center;">
                                    <span style="font-size: 18px; color: #9370DB;">Entropy</span>
                                    <div style="
                                        position: absolute;
                                        top: -35px;
                                        left: 50%;
                                        transform: translateX(-50%) rotate(-45deg);
                                        font-size: 30px;
                                        color: #9370DB;">
                                        &uarr;
                                    </div>
                                </div>
                                
                                <div style="position: relative; text-align: center;">
                                    <span style="font-size: 18px; color: #9370DB;">Conditional entropy</span>
                                    <div style="
                                        position: absolute;
                                        top: -35px;
                                        left: 30%;
                                        transform: translateX(-50%) rotate(-50deg);
                                        font-size: 30px;
                                        color: #9370DB;">
                                        &uarr;
                                    </div>
                                </div>
                            </div>
                        """)
                    )
                elif variables.get():
                    return ui.p(
                        ui.HTML("""  
                            <div style="text-align: center; font-size: 24px; font-weight: normal; color: #1F4A89;">
                                <span style="font-weight: bold;">Equation:</span> 
                                IG(<span style="color: #92D050;">Y</span>|<span style="color: #F79709;">X</span>) 
                                <span style="color: #1F4A89;">=</span> 
                                H(<span style="color: #92D050;">Y</span>) 
                                <span style="color: #1F4A89;">-</span> 
                                H(<span style="color: #92D050;">Y</span>|<span style="color: #F79709;">X</span>)
                            </div>
                            
                            <div style="display: flex; justify-content: center;">
                                <div style="position: relative; text-align: center; margin-left: 220px;">
                                    <span style="font-size: 18px; color: #92D050;">Output class (e.g. orange or lemon)</span>
                                    <div style="
                                        position: absolute;
                                        top: -35px;
                                        left: 60%;
                                        transform: translateX(-50%) rotate(5deg);
                                        font-size: 30px;
                                        color: #92D050;">
                                        &uarr;
                                    </div>
                                </div>
                                
                                <div style="position: relative; text-align: center;">
                                    <span style="font-size: 18px; color: #F79709;">Which side of the split the datapoint is on (e.g. left or right)</span>
                                    <div style="
                                        position: absolute;
                                        top: -35px;
                                        left: 40%;
                                        transform: translateX(-50%) rotate(-25deg);
                                        font-size: 30px;
                                        color: #F79709;">
                                        &uarr;
                                    </div>
                                </div>
                            </div>
                        """)
                    )
                elif definition.get():
                    return ui.p(
                        ui.HTML("""
                            <div style="text-align: center; font-size: 24px; font-weight: normal; color: #1F4A89;">
                                <span style="font-weight: bold;">Equation:</span> 
                                IG(Y|X) = H(Y) - H(Y|X)
                            </div>
                            
                            <div style="text-align: center; font-size: 18px; font-weight: normal; color: #1F4A89;">
                                This is the equation for information gain. It tells us how much information is gained about Y after observing X. In other words, how much uncertainty (entropy) is reduced by our chosen split.
                            </div>
                            
                            <div style="text-align: left; font-size: 18px; font-weight: normal; color: #1F4A89;">
                                Entropy H(Y): Characterizes the uncertainty in a draw of a random variable<br>
                                Conditional Entropy H(Y|X): Characterizes the uncertainty in a draw of Y after observing X<br>
                                Information Gain IG(Y|X): How much information is gained about Y after observing X
                            </div>
                        """)
                    )
                else:
                    return ui.p(
                        ui.HTML("""
                            <div style="text-align: center; font-size: 24px; font-weight: normal; color: #1F4A89;">
                                <span style="font-weight: bold;">Equation:</span>
                                IG(Y|X) = H(Y) - H(Y|X)
                            </div>
                        """)
                    )
            ui.div(style="flex-grow: 1;")
            # Text to display information gain
            @render.ui()
            @reactive.event(input.calculate_button)
            def calculate():
                side1 = "left" if vertical_split.get() else "below"
                side2 = "right" if vertical_split.get() else "above"
                side1_orange = 0
                side2_orange = 0
                side1_lemon = 0
                side2_lemon = 0
                for (x, y) in zip(o_points.get()['x'], o_points.get()['y']):
                    if (vertical_split.get() and x < split_loc.get()) or (not vertical_split.get() and y < split_loc.get()):
                        side1_orange += 1
                    else:
                        side2_orange += 1
                for (x, y) in zip(l_points.get()['x'], l_points.get()['y']):
                    if (vertical_split.get() and x < split_loc.get()) or (not vertical_split.get() and y < split_loc.get()):
                        side1_lemon += 1
                    else:
                        side2_lemon += 1
                oranges = side1_orange + side2_orange
                lemons = side1_lemon + side2_lemon
                total = oranges + lemons
                side1s = side1_orange + side1_lemon
                side2s = side2_orange + side2_lemon
                h_y = calculate_entropy(lemons, oranges, total)
                h_yside1 = calculate_entropy(side1_lemon, side1_orange, side1s)
                h_yside2 = calculate_entropy(side2_lemon, side2_orange, side2s)
                h_yx = calculate_condent(side1s, side2s, total, h_yside1, h_yside2)
                infogain = calculate_infogain(h_y, h_yx)
                info = {'side1': side1, 'side2': side2, 'side1_orange': side1_orange,
                        'side2_orange': side2_orange, 'side1_lemon': side1_lemon, 'side2_lemon': side2_lemon,
                        'oranges': oranges, 'lemons': lemons, 'total': total,
                        'side1s': side1s, 'side2s': side2s, 'h_y': h_y,
                        'h_yside1': h_yside1, 'h_yside2': h_yside2, 'h_yx': h_yx,
                        'infogain': infogain}
                print(step.get())
                return ui.p(
                        ui.HTML(create_mathjax_content(info))
                    )

            @render.ui()
            def calculate_test():
                side1 = "left" if vertical_split.get() else "below"
                side2 = "right" if vertical_split.get() else "above"
                side1_orange = 0
                side2_orange = 0
                side1_lemon = 0
                side2_lemon = 0
                for (x, y) in zip(o_points.get()['x'], o_points.get()['y']):
                    if (vertical_split.get() and x < split_loc.get()) or (not vertical_split.get() and y < split_loc.get()):
                        side1_orange += 1
                    else:
                        side2_orange += 1
                for (x, y) in zip(l_points.get()['x'], l_points.get()['y']):
                    if (vertical_split.get() and x < split_loc.get()) or (not vertical_split.get() and y < split_loc.get()):
                        side1_lemon += 1
                    else:
                        side2_lemon += 1
                oranges = side1_orange + side2_orange
                lemons = side1_lemon + side2_lemon
                total = oranges + lemons
                side1s = side1_orange + side1_lemon
                side2s = side2_orange + side2_lemon
                h_y = calculate_entropy(lemons, oranges, total)
                h_yside1 = calculate_entropy(side1_lemon, side1_orange, side1s)
                h_yside2 = calculate_entropy(side2_lemon, side2_orange, side2s)
                h_yx = calculate_condent(side1s, side2s, total, h_yside1, h_yside2)
                infogain = calculate_infogain(h_y, h_yx)
                if not input.calculate_button():
                    return ui.p(
                            ui.HTML(f"""
                                <script type="text/javascript" async 
                                    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
                                </script>
                                    
                                <div style="text-align: center; font-size: 17px; font-weight: normal; color: #1F4A89; line-height: 1;">
                                    \\[H(Y) = -\\frac{lemons}{total}log_{2}\\frac{lemons}{total} -\\frac{oranges}{total}log_{2}\\frac{oranges}{total}\\approx{h_y}\\]<br>
                                    \\[H(Y|{side1}) = -\\frac{side1_lemon}{side1s}log_{2}\\frac{side1_lemon}{side1s} -\\frac{side1_orange}{side1s}log_{2}\\frac{side1_orange}{side1s}\\approx{h_yside1}\\]<br>
                                    \\[H(Y|{side2}) = -\\frac{side2_lemon}{side2s}log_{2}\\frac{side2_lemon}{side2s} -\\frac{side2_orange}{side2s}log_{2}\\frac{side2_orange}{side2s}\\approx{h_yside2}\\]<br>
                                    \\[H(Y|X) = \\frac{side1s}{total}\\cdot{h_yside1} + \\frac{side2s}{total}\\cdot{h_yside2}\\approx{h_yx}\\]<br>
                                    \\[IG(Y|X) = {h_y} - {h_yx} \\approx {infogain}\\]
                                </div>
                                    
                                <script type="text/javascript">
                                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                                </script>
                            """)
                        )

            # Button to calculate information gain
            with ui.layout_columns():
                ui.div(
                    ui.input_action_button("notation", "Toggle notation", style="color: #fff; background-color: #337ab7; border-color: #2e6da4;"),
                    ui.input_action_button("variables", "Toggle variables", style="color: #fff; background-color: #337ab7; border-color: #2e6da4;"),
                    ui.input_action_button("definition", "Toggle definition", style="color: #fff; background-color: #337ab7; border-color: #2e6da4;"),
                    style="display: flex; justify-content: space-between; gap: 10px; margin-top: auto;"
                ),
            # Toggle buttons for notation, variables, and definition
            @reactive.effect
            @reactive.event(input.notation)
            def toggle_notation():
                notation.set(not notation.get())
                variables.set(False)
                definition.set(False)
                
            @reactive.effect
            @reactive.event(input.variables)
            def toggle_variables():
                variables.set(not variables.get())
                notation.set(False)
                definition.set(False)
            @reactive.effect
            @reactive.event(input.definition)
            def toggle_definition():
                definition.set(not definition.get())
                notation.set(False)
                variables.set(False)
            
            ui.div(
                ui.div(
                    ui.input_action_button("calculate_button", "Calculate information gain", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                    ui.input_action_button("prev_step", "Previous step", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                    ui.input_action_button("next_step", "Next step", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                    style="display: flex; justify-content: space-between; gap: 10px; margin-top: auto;"
                ),
            ),

            @reactive.effect
            @reactive.event(input.prev_step)
            def go_back():
                step.set(max(0, step.get()-1))
            
            @reactive.effect
            @reactive.event(input.next_step)
            def go_forward():
                step.set(min(5, step.get()+1))
                print(step.get())