from shiny import reactive, render
from shiny.express import input, ui
import plotly.graph_objects as go
from shinywidgets import render_plotly
import math

# Calculation helper functions
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

# Create the information gain calculations in mathjax
# Show equations corresponding to what step of the calculation the user is on
def create_mathjax_content(info):
    lines = {
        1: f"""
            <div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89; line-height: 1;">
                <span>\\(H(\\)</span>
                {tooltip_test("Y", f"(Oranges, Lemons)", f"Y")}
                <span>\\()=-\\)</span>
                {tooltip_test("Total lemons", "Total lemons / Total datapoints", f"\\frac{info['lemons']}{info['total']} \\log_{2} \\frac{info['lemons']}{info['total']}")}
                <span>\\(-\\)</span>
                {tooltip_test("Total oranges", "Total oranges / Total datapoints", f"\\frac{info['oranges']}{info['total']} \\log_{2} \\frac{info['oranges']}{info['total']}")}
                <span>\\( \\approx{info['h_y']} \\)
            </div>

            <script>
                document.getElementById("Total lemons").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_all_lemons", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Total lemons").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_all_lemons", "Not Hovered", {{priority: "event"}});
                }});

                document.getElementById("Total oranges").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_all_oranges", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Total oranges").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_all_oranges", "Not Hovered", {{priority: "event"}});
                }});

                updateMathJax();
            </script>
        """,
        2: f"""
            <div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89; line-height: 1;">
                <span>\\(H(\\)</span>
                {tooltip_test("Y", f"Oranges, Lemons", f"Y")}
                <span>\\(|\\)</span>
                {tooltip_test("X side 1", f"Only looking at the {info['side1']} side of the split", f"X = {info['side1']}")}
                <span>\\()=-\\)</span>
                {tooltip_test("Lemons side 1", f"Total lemons {info['side1']} / Total datapoints {info['side1']}", f"\\frac{info['side1_lemon']}{info['side1s']} \\log_{2} \\frac{info['side1_lemon']}{info['side1s']}")}
                <span>\\(-\\)</span>
                {tooltip_test("Oranges side 1", f"Total oranges {info['side1']} / Total datapoints {info['side1']}", f"\\frac{info['side1_orange']}{info['side1s']} \\log_{2} \\frac{info['side1_orange']}{info['side1s']}")}
                <span>\\( \\approx{info['h_yside1']} \\)
            </div>

            <script>
                document.getElementById("X side 1").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_X_side1", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("X side 1").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_X_side1", "Not Hovered", {{priority: "event"}});
                }});

                document.getElementById("Lemons side 1").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_lemons_side1", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Lemons side 1").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_lemons_side1", "Not Hovered", {{priority: "event"}});
                }});

                document.getElementById("Oranges side 1").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_oranges_side1", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Oranges side 1").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_oranges_side1", "Not Hovered", {{priority: "event"}});
                }});

                updateMathJax();
            </script>
        """,
        3: f"""
            <div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89; line-height: 1;">
                <span>\\(H(\\)</span>
                {tooltip_test("Y", f"Oranges, Lemons", f"Y")}
                <span>\\(|\\)</span>
                {tooltip_test("X side 2", f"Only looking at the {info['side2']} side of the split", f"X = {info['side2']}")}
                <span>\\()=-\\)</span>
                {tooltip_test("Lemons side 2", f"Total lemons {info['side2']} / Total datapoints {info['side2']}", f"\\frac{info['side2_lemon']}{info['side2s']} \\log_{2} \\frac{info['side2_lemon']}{info['side2s']}")}
                <span>\\(-\\)</span>
                {tooltip_test("Oranges side 2", f"Total oranges {info['side2']} / Total datapoints {info['side2']}", f"\\frac{info['side2_orange']}{info['side2s']} \\log_{2} \\frac{info['side2_orange']}{info['side2s']}")}
                <span>\\( \\approx{info['h_yside2']} \\)
            </div>

            <script>
                document.getElementById("X side 2").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_X_side2", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("X side 2").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_X_side2", "Not Hovered", {{priority: "event"}});
                }});

                document.getElementById("Lemons side 2").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_lemons_side2", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Lemons side 2").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_lemons_side2", "Not Hovered", {{priority: "event"}});
                }});

                document.getElementById("Oranges side 2").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_oranges_side2", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Oranges side 2").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_oranges_side2", "Not Hovered", {{priority: "event"}});
                }});

                updateMathJax();
            </script>
        """,
        4: f"""
            <div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89; line-height: 1;">
                <span>\\(H(\\)</span>
                {tooltip_test("Y", f"Oranges, Lemons", f"Y")}
                <span>\\(|\\)</span>
                {tooltip_test("X", f"{info['side1']}, {info['side2']}", f"X")}
                <span>\\()=\\)</span>
                {tooltip_test("Side 1", f"Total {info['side1']} datapoints / Total datapoints", f"\\frac{info['side1s']}{info['total']}")}
                <span>\\(\\cdot\\)</span>
                {tooltip_test("Hy Side 1", f"H(Y|X={info['side1']})", f"{info['h_yside1']}")}
                <span>\\(+\\)</span>
                {tooltip_test("Side 2", f"Total {info['side2']} datapoints / Total datapoints", f"\\frac{info['side2s']}{info['total']}")}
                <span>\\(\\cdot\\)</span>
                {tooltip_test("Hy Side 2", f"H(Y|X={info['side2']})", f"{info['h_yside2']}")}
                <span>\\( \\approx{info['h_yx']} \\)
            </div>

            <script>
                document.getElementById("Side 1").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_side1", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Side 1").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_side1", "Not Hovered", {{priority: "event"}});
                }});

                document.getElementById("Side 2").addEventListener("mouseenter", function() {{
                    Shiny.setInputValue("btn_side2", "Hovered", {{priority: "event"}});
                }});
                document.getElementById("Side 2").addEventListener("mouseleave", function() {{
                    Shiny.setInputValue("btn_side2", "Not Hovered", {{priority: "event"}});
                }});

                updateMathJax();
            </script>
        """,
        5: f"""
            <div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89; line-height: 1;">
                {tooltip_test("infogain", f"Information gain from this split", f"IG(Y|X)")}
                <span>\\(=\\)</span>
                {tooltip_test("Hy", f"H(Y)", f"{info['h_y']}")}
                <span>\\(-\\)</span>
                {tooltip_test("Hyx", f"H(Y|X)", f"{info['h_yx']}")}
                <span>\\(\\approx {info['infogain']}\\)</span>
            </div>
        """,
        6: f"""
            <div style="text-align: center; font-size: 20px; font-weight: normal; color: #fff; line-height: 1;">
                <span>\\(IG(Y|X)\\)</span>
            </div>
        """
    }
    
    # Start the HTML content
    mathjax_html = """"""
    
    # Add the selected line based on the `step`
    for i in range(1, 6):
        if i <= step.get():
            mathjax_html += lines[i]
    # Add blank spacing to keep formatting the same
    for i in range(5-step.get()):
        mathjax_html += lines[6]
    
    return mathjax_html

# Starter datapoints to plot and other reactive value setups
o_points = reactive.value({'x': [1, 1, 5, 8, 8], 'y': [3, 7, 7, 4, 7]})
l_points = reactive.value({'x': [5, 8], 'y': [4, 3]})
x_coord = reactive.value(0)
y_coord = reactive.value(0)
vertical_split = reactive.value(True)
split_loc = reactive.value(3)
o_outline_width = reactive.value([0, 0, 0, 0, 0])
l_outline_width = reactive.value([0, 0])
step = reactive.value(5)
rect_coords = reactive.value([0, 0, 0, 0])
notation = reactive.value(False)
variables = reactive.value(False)
definition = reactive.value(False)

# Make main screen with title
ui.page_opts(
    title="Decision Trees",  
    fillable=True,
)

# Setting up styling and scripts
ui.HTML("""
    <script type="text/javascript" async 
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>

    <style>
        .tooltip-custom {
            position: relative;
            display: inline-block;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out;
        }

        .tooltip-custom:hover {
            background-color:rgb(247, 186, 186);  /* Light background color to highlight */
            border-radius: 5px;  /* Optional: smooth rounded edges */
        }

        .tooltip-custom::after {
            content: attr(data-tooltip);
            position: absolute;
            background-color: black;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            top: 120%;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            font-size: 14px;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease-in-out;
        }

        .tooltip-custom:hover::after {
            opacity: 1;
            visibility: visible;
        }
    </style>

    <script>
        // Function to update MathJax rendering when new Shiny data is available
        function updateMathJax() {
            if (window.MathJax) {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            }
        }
        document.addEventListener("shiny:value", updateMathJax);
    </script>


    <script>
        // Re-render MathJax on hover over the tooltip
        document.querySelectorAll('data-tooltip').forEach(function(tooltip) {
            tooltip.addEventListener('mouseenter', function() {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            });
        });
    </script>
""")


# Sidebar for coordinate and split selection
with ui.sidebar(open="open", bg="#f8f8f8"):
    ui.HTML('<b>Datapoint Selection</b>')

    ui.div(
        ui.input_numeric("xcoord", "Width in cm (0-10)", 1, min=0, max=10),
        ui.input_numeric("ycoord", "Height in cm (0-10)", 1, min=0, max=10),
        ui.input_select("select_add", "Select what datapoint to add:", {"Orange": "Orange", "Lemon": "Lemon"}),
        ui.input_action_button("add_dp", "Add", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%; heigth: 70%;"),
        class_="gap-0 mb-0"
    )

    @reactive.effect
    @reactive.event(input.xcoord)
    def yvalue():
        x_coord.set(input.xcoord())
    
    @reactive.effect
    @reactive.event(input.ycoord)
    def yvalue():
        y_coord.set(input.ycoord())
    
    @render.text()
    def error_check():
        if not isinstance(input.ycoord(), int):
            return "Invalid input"

    @reactive.effect
    @reactive.event(input.add_dp)
    def add_dp():
        if input.select_add() == "Orange":
            curr_points = o_points.get()
            updated_points = {
                'x': curr_points['x'] + [x_coord.get()],
                'y': curr_points['y'] + [y_coord.get()],
            }
            o_points.set(updated_points)
            o_outline_width.get().append(0)
        else:
            curr_points = l_points.get()
            updated_points = {
                'x': curr_points['x'] + [x_coord.get()],
                'y': curr_points['y'] + [y_coord.get()],
            }
            l_points.set(updated_points)
            l_outline_width.get().append(0)
    
    ui.hr(style="margin-top: 5px; margin-bottom: 5px;"),

    ui.HTML('<b>Datapoint Removal</b>')

    ui.div(
        ui.input_select("select_remove", "Select a datapoint to remove (the latest one will be removed):", {"Orange": "Orange", "Lemon": "Lemon"}),
        ui.input_action_button("remove_dp", "Remove", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%; heigth: 70%;"),
        class_="gap-0"
    )

    @reactive.effect
    @reactive.event(input.remove_dp)
    def remove_dp():
        if input.select_remove() == "Orange":
            curr_points = o_points.get()
            if len(curr_points['x']) > 0:
                curr_points['x'].pop()
                curr_points['y'].pop()
                updated_points = {
                    'x': curr_points['x'],
                    'y': curr_points['y'],
                }
                o_points.set(updated_points)
                o_outline_width.get().pop()
        else:
            curr_points = l_points.get()
            if len(curr_points['x']) > 0:
                curr_points['x'].pop()
                curr_points['y'].pop()
                updated_points = {
                    'x': curr_points['x'],
                    'y': curr_points['y'],
                }
                l_points.set(updated_points)
                l_outline_width.get().pop()

    ui.hr(style="margin-bottom: 5px;"),

    ui.HTML('<b>Split Selection</b>')
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

with ui.layout_columns():
    # Dataset card
    with ui.card():
        ui.card_header("Dataset", style="font-size: 20px;")
        # Plot where students will be putting datapoints and split
        @render_plotly
        def feature_plot():
            fig = go.Figure()
            # fig.update_layout(
            #     height=400,
            #     width=700,
            #     margin=dict(t=10, b=10, l=10, r=10)  # Adjust the margins if needed
            # )
            # Highlights from tooltip
            fig.add_shape(
                type="rect",
                x0=rect_coords.get()[0],
                x1=rect_coords.get()[1],
                y0=rect_coords.get()[2],
                y1=rect_coords.get()[3],
                fillcolor="yellow",
                opacity=0.2
            )
            # Orange points
            fig.add_trace(go.Scatter(
                x=o_points.get()['x'],
                y=o_points.get()['y'],
                mode='markers',
                name='Orange',
                marker=dict(
                    color='#E54C38',
                    size=12,
                    symbol='circle',
                    line=dict(
                        color=['black']*len(o_outline_width.get()),  # Outline for some points
                        width=o_outline_width.get()  # 0 width removes outline for some points
                    )
                )
            ))
            # Lemon points
            fig.add_trace(go.Scatter(
                x=l_points.get()['x'],
                y=l_points.get()['y'],
                mode='markers',
                name='Lemon',
                marker=dict(
                    color='#4A75D4',
                    size=12,
                    symbol='triangle-up',
                    line=dict(
                        color=['black']*len(l_outline_width.get()),  # Outline for some points
                        width=l_outline_width.get()  # 0 width removes outline for some points
                    )
                )
            ))
            # Make plot
            fig.update_layout(
                xaxis=dict(
                    range=[0, 10],
                    fixedrange=True,  # Locks zooming
                    showgrid=True,
                    gridcolor='rgba(0, 0, 0, 0.1)',
                    gridwidth=1
                ),
                yaxis=dict(
                    range=[0, 10],
                    fixedrange=True,  # Locks zooming
                    showgrid=True,
                    gridcolor='rgba(0, 0, 0, 0.1)',
                    gridwidth=1
                ),
                xaxis_title="Width",
                yaxis_title="Height",
                showlegend=True,
                plot_bgcolor='white',
                dragmode=False,  # Disables all drag interactions
                modebar=dict(
                    remove=["select2d", "lasso2d"]
                )
            )

            # Split location
            if (vertical_split.get()):
                fig.add_vline(x=split_loc.get(), line=dict(color="purple", width=2, dash="dash"), name="Vertical Line")
            else:
                fig.add_hline(y=split_loc.get(), line=dict(color="purple", width=2, dash="dash"), name="Horizontal Line")
            
            return fig
        
        # Buttons to add datapoints

    # Calculations card
    with ui.card():
        ui.card_header(
            ui.HTML('Calculations <br> <i><span style="font-weight: normal; font-size: 16px;">(Hover over components of the equation to see where the numbers come from!)</span></i>'),
            style="font-size: 20px;"
        )
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
                            <div style="position: relative; text-align: center; margin-left: 150px;">
                                <span style="font-size: 18px; color: #92D050;">Output class (e.g. orange or lemon)</span>
                                <div style="
                                    position: absolute;
                                    top: -35px;
                                    left: 70%;
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
                                    left: 58%;
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
                            <u>Entropy H(Y):</u> Characterizes the uncertainty in a draw of a random variable<br>
                            <u>Conditional Entropy H(Y|X):</u> Characterizes the uncertainty in a draw of Y after observing X<br>
                            <u>Information Gain IG(Y|X):</u> How much information is gained about Y after observing X
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
        
        # Helper function to calculate information gain
        def calculate():
            valid = 1
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
            if side1s == 0 or side2s == 0:
                valid = 0
                info = {'valid': valid}
            else:
                h_y = calculate_entropy(lemons, oranges, total)
                h_yside1 = calculate_entropy(side1_lemon, side1_orange, side1s)
                h_yside2 = calculate_entropy(side2_lemon, side2_orange, side2s)
                h_yx = calculate_condent(side1s, side2s, total, h_yside1, h_yside2)
                infogain = calculate_infogain(h_y, h_yx)
                info = {'valid': valid, 'side1': side1, 'side2': side2, 'side1_orange': side1_orange,
                        'side2_orange': side2_orange, 'side1_lemon': side1_lemon, 'side2_lemon': side2_lemon,
                        'oranges': oranges, 'lemons': lemons, 'total': total,
                        'side1s': side1s, 'side2s': side2s, 'h_y': h_y,
                        'h_yside1': h_yside1, 'h_yside2': h_yside2, 'h_yx': h_yx,
                        'infogain': infogain}
            return info

        # Helper function to make tooltips
        def tooltip_test(id, tip, content):
            return f"""<span id="{id}" class="tooltip-custom" data-tooltip="{tip}">\\( {content} \\)</span>"""

        # Render calculations
        @render.ui
        def calculations_mathjax():
            info = calculate()
            if info['valid'] == 1:
                return ui.HTML(create_mathjax_content(info))
            else:
                return ui.HTML('<div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89; line-height: 1;">Invalid split - no information is gained from this split!</div>')
        
        # All these functions are to make correspondings changes to the plot based on user mouse hovering (tooltips)
        @reactive.effect
        @reactive.event(input.btn_side2)
        def highlight_side1():
            tooltip_state = input.btn_side2()
            o_copy = o_outline_width.get()[:]
            l_copy = l_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]

            if tooltip_state == "Hovered":
                for i in range(len(o_copy)):
                    if vertical_split.get() == True and o_points.get()['x'][i] > split_loc.get():
                        o_copy[i] = 2
                    if vertical_split.get() == False and o_points.get()['y'][i] > split_loc.get():
                        o_copy[i] = 2
                for i in range(len(l_copy)):
                    if vertical_split.get() == True and l_points.get()['x'][i] > split_loc.get():
                        l_copy[i] = 2  # Change outline width to 2 when hovered
                    if vertical_split.get() == False and l_points.get()['y'][i] > split_loc.get():
                        l_copy[i] = 2
            
                rect_copy[0] = 0
                rect_copy[1] = 10
                rect_copy[2] = 0
                rect_copy[3] = 10
                rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                for i in range(len(o_copy)):
                    o_copy[i] = 0
                for i in range(len(l_copy)):
                    l_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            o_outline_width.set(o_copy)
            l_outline_width.set(l_copy)

        @reactive.effect
        @reactive.event(input.btn_side1)
        def highlight_side1():
            tooltip_state = input.btn_side1()
            o_copy = o_outline_width.get()[:]
            l_copy = l_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]

            if tooltip_state == "Hovered":
                for i in range(len(o_copy)):
                    if vertical_split.get() == True and o_points.get()['x'][i] < split_loc.get():
                        o_copy[i] = 2
                    if vertical_split.get() == False and o_points.get()['y'][i] < split_loc.get():
                        o_copy[i] = 2
                for i in range(len(l_copy)):
                    if vertical_split.get() == True and l_points.get()['x'][i] < split_loc.get():
                        l_copy[i] = 2  # Change outline width to 2 when hovered
                    if vertical_split.get() == False and l_points.get()['y'][i] < split_loc.get():
                        l_copy[i] = 2
            
                rect_copy[0] = 0
                rect_copy[1] = 10
                rect_copy[2] = 0
                rect_copy[3] = 10
                rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                for i in range(len(o_copy)):
                    o_copy[i] = 0
                for i in range(len(l_copy)):
                    l_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            o_outline_width.set(o_copy)
            l_outline_width.set(l_copy)

        @reactive.effect
        @reactive.event(input.btn_oranges_side2)
        def highlight_orange_side2():
            tooltip_state = input.btn_oranges_side2()
            o_copy = o_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]

            if tooltip_state == "Hovered":
                for i in range(len(o_copy)):
                    if vertical_split.get() == True and o_points.get()['x'][i] >= split_loc.get():
                        o_copy[i] = 2
                    if vertical_split.get() == False and o_points.get()['y'][i] >= split_loc.get():
                        o_copy[i] = 2
                if vertical_split.get() == True:
                    rect_copy[0] = 10
                    rect_copy[1] = split_loc.get()
                    rect_copy[2] = 10
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
                else:
                    rect_copy[0] = 0
                    rect_copy[1] = 10
                    rect_copy[2] = split_loc.get()
                    rect_copy[3] = 10
                    rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                for i in range(len(o_copy)):
                    o_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            o_outline_width.set(o_copy)

        @reactive.effect
        @reactive.event(input.btn_lemons_side2)
        def highlight_lemons_side2():
            tooltip_state = input.btn_lemons_side2()
            # Get the current outline width
            l_copy = l_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]
            
            if tooltip_state == "Hovered":
                # Logic for when the tooltip is hovered
                for i in range(len(l_copy)):
                    if vertical_split.get() == True and l_points.get()['x'][i] >= split_loc.get():
                        l_copy[i] = 2  # Change outline width to 2 when hovered
                    if vertical_split.get() == False and l_points.get()['y'][i] >= split_loc.get():
                        l_copy[i] = 2
                if vertical_split.get() == True:
                    rect_copy[0] = 10
                    rect_copy[1] = split_loc.get()
                    rect_copy[2] = 10
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
                else:
                    rect_copy[0] = 0
                    rect_copy[1] = 10
                    rect_copy[2] = split_loc.get()
                    rect_copy[3] = 10
                    rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                # Logic for when the tooltip is not hovered
                for i in range(len(l_copy)):
                    l_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)

            # Set the updated outline width
            l_outline_width.set(l_copy)
        
        @reactive.effect
        @reactive.event(input.btn_X_side2)
        def highlight_side2():
            tooltip_state = input.btn_X_side2()
            rect_copy = rect_coords.get()[:]
            
            if tooltip_state == "Hovered":
                if vertical_split.get() == True:
                    rect_copy[0] = 10
                    rect_copy[1] = split_loc.get()
                    rect_copy[2] = 10
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
                else:
                    rect_copy[0] = 0
                    rect_copy[1] = 10
                    rect_copy[2] = split_loc.get()
                    rect_copy[3] = 10
                    rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)

        @reactive.effect
        @reactive.event(input.btn_oranges_side1)
        def highlight_orange_side1():
            tooltip_state = input.btn_oranges_side1()
            o_copy = o_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]

            if tooltip_state == "Hovered":
                for i in range(len(o_copy)):
                    if vertical_split.get() == True and o_points.get()['x'][i] < split_loc.get():
                        o_copy[i] = 2
                    if vertical_split.get() == False and o_points.get()['y'][i] < split_loc.get():
                        o_copy[i] = 2
                if vertical_split.get() == True:
                    rect_copy[0] = 0
                    rect_copy[1] = split_loc.get()
                    rect_copy[2] = 10
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
                else:
                    rect_copy[0] = 0
                    rect_copy[1] = 10
                    rect_copy[2] = split_loc.get()
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                for i in range(len(o_copy)):
                    o_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            o_outline_width.set(o_copy)

        @reactive.effect
        @reactive.event(input.btn_lemons_side1)
        def highlight_lemons_side1():
            tooltip_state = input.btn_lemons_side1()
            # Get the current outline width
            l_copy = l_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]
            
            if tooltip_state == "Hovered":
                # Logic for when the tooltip is hovered
                for i in range(len(l_copy)):
                    if vertical_split.get() == True and l_points.get()['x'][i] < split_loc.get():
                        l_copy[i] = 2  # Change outline width to 2 when hovered
                    if vertical_split.get() == False and l_points.get()['y'][i] < split_loc.get():
                        l_copy[i] = 2
                if vertical_split.get() == True:
                    rect_copy[0] = 0
                    rect_copy[1] = split_loc.get()
                    rect_copy[2] = 10
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
                else:
                    rect_copy[0] = 0
                    rect_copy[1] = 10
                    rect_copy[2] = split_loc.get()
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                # Logic for when the tooltip is not hovered
                for i in range(len(l_copy)):
                    l_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)

            # Set the updated outline width
            l_outline_width.set(l_copy)
        
        @reactive.effect
        @reactive.event(input.btn_X_side1)
        def highlight_side1():
            tooltip_state = input.btn_X_side1()
            rect_copy = rect_coords.get()[:]
            
            if tooltip_state == "Hovered":
                if vertical_split.get() == True:
                    rect_copy[0] = 0
                    rect_copy[1] = split_loc.get()
                    rect_copy[2] = 10
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
                else:
                    rect_copy[0] = 0
                    rect_copy[1] = 10
                    rect_copy[2] = split_loc.get()
                    rect_copy[3] = 0
                    rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)

        @reactive.effect
        @reactive.event(input.btn_all_lemons)
        def highlight_all_lemons():
            tooltip_state = input.btn_all_lemons()
            l_copy = l_outline_width.get()[:]   
            rect_copy = rect_coords.get()[:]
            if tooltip_state == "Hovered":
                for i in range(len(l_copy)):
                        l_copy[i] = 2
                rect_copy[0] = 0
                rect_copy[1] = 10
                rect_copy[2] = 10
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                for i in range(len(l_copy)):
                    l_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            l_outline_width.set(l_copy)

        @reactive.effect
        @reactive.event(input.btn_all_oranges)
        def highlight_all_oranges():
            tooltip_state = input.btn_all_oranges()
            o_copy = o_outline_width.get()[:]
            rect_copy = rect_coords.get()[:]
            if tooltip_state == "Hovered":
                for i in range(len(o_copy)):
                    o_copy[i] = 2
                rect_copy[0] = 0
                rect_copy[1] = 10
                rect_copy[2] = 10
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            elif tooltip_state == "Not Hovered":
                for i in range(len(o_copy)):
                    o_copy[i] = 0
                rect_copy[0] = 0
                rect_copy[1] = 0
                rect_copy[2] = 0
                rect_copy[3] = 0
                rect_coords.set(rect_copy)
            o_outline_width.set(o_copy)
        
        # Button to calculate information gain
        ui.div(
            ui.div(
                ui.input_action_button("notation", "Toggle notation", style="color: #fff; background-color: #337ab7; border-color: #2e6da4;"),
                ui.input_action_button("variables", "Toggle variables", style="color: #fff; background-color: #337ab7; border-color: #2e6da4;"),
                ui.input_action_button("definition", "Toggle definition", style="color: #fff; background-color: #337ab7; border-color: #2e6da4;"),
                style="display: flex; justify-content: space-between; gap: 10px;"
            ),
        ),
        
        ui.div(
            ui.div(
                ui.input_action_button("prev_step", "Previous step", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                ui.input_action_button("next_step", "Next step", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                style="display: flex; justify-content: space-between; gap: 10px;"
            ),
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

        @reactive.effect
        @reactive.event(input.prev_step)
        def go_back():
            step.set(max(0, step.get()-1))
        
        @reactive.effect
        @reactive.event(input.next_step)
        def go_forward():
            step.set(min(5, step.get()+1))
            print(step.get())