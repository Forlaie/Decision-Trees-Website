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
    ui.HTML('<b>Datapoint Coordinate Selection</b>')

    ui.input_numeric("xcoord", "X-coordinate (0-10)", 1, min=0, max=10),
    @reactive.effect
    @reactive.event(input.xcoord)
    def yvalue():
        x_coord.set(input.xcoord())
    
    ui.input_numeric("ycoord", "Y-coordinate (0-10)", 1, min=0, max=10),
    @reactive.effect
    @reactive.event(input.ycoord)
    def yvalue():
        y_coord.set(input.ycoord())
    
    @render.text()
    def error_check():
        if not isinstance(input.ycoord(), int):
            return "Invalid coordinate"

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
            # Split location
            if (vertical_split.get()):
                fig.add_vline(x=split_loc.get(), line=dict(color="purple", width=2, dash="dash"), name="Vertical Line")
            else:
                fig.add_hline(y=split_loc.get(), line=dict(color="purple", width=2, dash="dash"), name="Horizontal Line")
            return fig
        
        # Buttons to add datapoints
        with ui.layout_columns():
            ui.input_action_button("add_orange_button", "Add orange datapoint", style="color: #fff; background-color: #E54C38; border-color: #E54C38")
            ui.input_action_button("add_lemon_button", "Add lemon datapoint", style="color: #fff; background-color: #4A75D4; border-color: #4A75D4")
        
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
            o_outline_width.get().append(0)
        
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
            l_outline_width.get().append(0)
        
        # Buttons to remove datapoints
        with ui.layout_columns():
            ui.input_action_button("remove_orange_button", "Remove orange datapoint", style="color: #fff; background-color: #E54C38; border-color: #E54C38")
            ui.input_action_button("remove_lemon_button", "Remove lemon datapoint", style="color: #fff; background-color: #4A75D4; border-color: #4A75D4")

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
                o_outline_width.get().pop()
        
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
                l_outline_width.get().pop()

    # Calculations card
    with ui.card():
        ui.card_header("Calculations", style="font-size: 20px;")
        @render.ui()
        # Shows equation
        def show_equation():
            return ui.p(
                ui.HTML(f"""
                    <div style="text-align: center; font-size: 20px; font-weight: normal; color: #1F4A89;">
                        <span>\\(Equation: \\)</span>
                        {tooltip_test("IGinfo", f"Information Gain: How much information is gained about Y after observing X", f"IG")}
                        <span>\\((\\)</span>
                        {tooltip_test("Yinfo", f"Output class (e.g. orange, lemon)", f"Y")}
                        <span>\\(|\\)</span>
                        {tooltip_test("Xinfo", f"The side of the split (e.g. left, right)", f"X")}
                        <span>\\()=\\)</span>
                        {tooltip_test("HYinfo", f"Entropy: The uncertainty of random variable Y", f"H(Y)")}
                        <span>\\(-\\)</span>
                        {tooltip_test("HYXinfo", f"Conditional Entropy: The uncertainty of random variable Y after observing X", f"H(Y|X)")}
                    </div>
                    
                    <script>                    
                        updateMathJax();
                    </script>
                """)
            )
        
        # Helper function to calculate information gain
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
            return info

        # Helper function to make tooltips
        def tooltip_test(id, tip, content):
            return f"""<span id="{id}" class="tooltip-custom" data-tooltip="{tip}">\\( {content} \\)</span>"""

        # Render calculations
        @render.ui
        def calculations_mathjax():
            info = calculate()
            return ui.HTML(create_mathjax_content(info))
        
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
                    if vertical_split.get() == True and o_points.get()['x'][i] > split_loc.get():
                        o_copy[i] = 2
                    if vertical_split.get() == False and o_points.get()['y'][i] > split_loc.get():
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
                    if vertical_split.get() == True and l_points.get()['x'][i] > split_loc.get():
                        l_copy[i] = 2  # Change outline width to 2 when hovered
                    if vertical_split.get() == False and l_points.get()['y'][i] > split_loc.get():
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
        
        # Step calculation buttons
        ui.div(
            ui.div(
                ui.input_action_button("prev_step", "Previous step", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                ui.input_action_button("next_step", "Next step", style="color: #fff; background-color: #337ab7; border-color: #2e6da4; width: 100%;"),
                style="display: flex; justify-content: space-between; gap: 10px; margin-top: auto;"
            ),
            style="display: flex; flex-direction: column; justify-content: flex-end; height: 20%;"  # Aligns the div to the bottom
        )

        # Logic for step calculations
        @reactive.effect
        @reactive.event(input.prev_step)
        def go_back():
            step.set(max(0, step.get()-1))
        
        @reactive.effect
        @reactive.event(input.next_step)
        def go_forward():
            step.set(min(5, step.get()+1))
            print(step.get())