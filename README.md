# Introduction #
A web-based visualization for Decision Tree Models, focusing specifically on the Information Gain calculation aspect.
This visualization demonstrates how information gain is computed for different datasets and split choices, emphasizing how the computation relates to the data.
For the sake of space and simplicity, the data is limited to 2D points within a 10×10 grid.

### User-interactivity ###
- Can add or remove datapoints of two different labels: oranges and lemons
- Splits can be placed horizontally or vertically within the 10x10 grid
- Toggle buttons to view notation explanations, variable definitions, and concept definitions if needed
- Hovering over different parts of the information gain equations will highlight the relevant datapoints used in that calculation, to demonstrate where the numbers are coming from and what we're trying to calculate
- Step-by-step walkthrough of calculations by using the "Previous step" and "Next step" buttons at the bottom
![{1D942340-F63A-42CB-B2D6-36969757B269}](https://github.com/user-attachments/assets/60729dad-b784-40cb-95a4-b63fe44600e4)

### Pre-requisite Knowledge ###
For users to fully benefit from this visualization, they should have a prior understanding of decision tree models, the algorithm used to construct them, and a basic grasp of entropy.
Otherwise, they won't understand the bigger picture behind why information gain calculations are important and how they relate to decision tree models.

# Installation #
```
git clone https://github.com/Forlaie/Decision-Trees-Website.git
pip install -r requirements.txt
cd Decision-Trees-Website
python app.py
```
# Technical Components #
This section is mostly focused on my code, as in how to use/add on to it, as well as warnings for coding challenges I faced using Python Shiny...

### MathJax Equation Content ###
All MathJax equations are stored and created in the function ```create_mathjax_content```, so if you wish to change the equations or add new text, do so there.
Note that they're all written in HTML with inline CSS. Also, if you're using MathJax and notice that your MathJax isn't rendering properly, you might want to include:
```
<script>
  updateMathJax();
</script>
```
after your ```</div>```.

This is because if you put ```updateMathJax()``` in the wrong place, it won't actually render all of your MathJax text.
From my experience, it seems that it works best to include ```updateMathJax()``` in your first instance of MathJax-rendered text, although I'm not sure exactly why that's the case.
Technically though, you can't go wrong with including it in your JavaScript for every MathJax text. 

Example of unrendered MathJax:
![{79E5A43C-3C47-480E-8054-96468C8DDD32}](https://github.com/user-attachments/assets/e3e984d5-b23f-40ef-b03e-0245ca814d3a)

### Tooltip Content ###
Tooltip texts are created using the helper function I made, called ```tooltip_test```.
To use this, inside your ```<div>```, include ```{tooltip_test("id", "tooltip text", "display text")}```.
Then, in order to be able to register that a user has hovered over your tooltip (and connect it to a button or whatever other component you'd like), you need:
```
<script>
  document.getElementById("id").addEventListener("mouseenter", function() {{
      Shiny.setInputValue("hovering_id", "Hovered", {{priority: "event"}});
  }});
  document.getElementById("id").addEventListener("mouseleave", function() {{
      Shiny.setInputValue("hovering_id", "Not Hovered", {{priority: "event"}});
  }});
</script>
```
after your ```</div>```,
where ```id``` should correspond to the id you passed into the ```tooltip_test``` function,
and ```hovering_id``` corresponds to the input value being set for that item.
With this input value, you can then make functions that will perform certain actions when the text is hovered, like such:
```
@reactive.effect
@reactive.event(input.hovering_id)
def do_stuff():
    tooltip_state = input.hovering_id()
    if tooltip_state == "Hovered":
        // do stuff
    else:
        // do other stuff
```
Note that each item's ```id``` and ```hovering_id``` must be unique.

Now, Python Shiny Express has a built-in tooltip, which can be used by calling ```ui.tooltip()```:
```
with ui.tooltip(id="btn_tooltip"):
    ui.input_action_button("btn", "A button", class_="mt-3")
    "Tooltip text"
```
However, the reason why I made my own helper function was because this built-in tooltip is very difficult to use and customize (do so at the risk of your own sanity...).
In particular, the biggest challenge I faced was trying to use reactive values within this built-in tooltip.
Essentially, what I was trying to do was to allow users to hover over specific aspects of the equation, which would then highlight corresponding aspects of the data.
Now, since all my calculations change as the user modifies the datapoints or makes a new split choice, all these numbers are calculated reactively.
However, ```ui.tooltip()``` is not a reactive environment, which basically just means that it can't work with reactive values; it can only work with static.
So, if you wanted to create a tooltip for something that is hard-coded, you can use ```ui.tooltip()```.
Otherwise, you should use the helper function I've made.

Another big issue with tooltips is that there is no easy way to have the tooltip only correspond to a certain part of your text (e.g. if you had a sentence and only wanted one word to be hoverable with tooltips).
Hence, I just use a *(admittedly crude)* work-around for this situation. For example, if I want to have the text H(Y) displayed on screen, with only Y being hoverable, I would do this in my JavaScript:
```
  <span>\\(H(\\)</span>
  {tooltip_test("Y", f"Oranges, Lemons", f"Y")}
  <span>\\()\\)</span>
```
Essentially, I create a separate piece of text every time I want to change from tooltip text to non-tooltip text, and then mash everything together in JavaScript so that all the texts are displayed in one line as desired.

# Other Features #
This section is mostly about how I've implemented different features of my visualization, such as how I handle datapoints and the graph.
There's far less emphasis on my code and how it works, or why I made certain decisions.

### Datapoint Modification ###
Currently, I have my datapoint information stored as reactive values, like such:
```
o_points = reactive.value({'width': [1, 1, 5, 8, 8], 'height': [3, 7, 7, 4, 7]})
l_points = reactive.value({'width': [5, 8], 'height': [4, 3]})
```
This is because I want the plotly graph to change reactively, as users add or remove datapoints.
If you want to add any new features that will update automatically, you must use ```reactive.value```.
To get the value, you then use ```var_name.get()```, and to change it, you use ```var_name.set(new_value)```.  
BE CAREFUL IN THE CASE OF DICTIONARIES AND LISTS!!!
With Python Shiny Express, reactive values only detect changes when the memory location they reference is updated.
So, for example, if you want to add a new point to o_points and have it register, you *must* make a new dictionary and reassign its value:
```
curr_points = o_points.get()
updated_points = {
    'x': curr_points['x'] + [x_coord.get()],
    'y': curr_points['y'] + [y_coord.get()],
}
o_points.set(updated_points)
```

### Plotly Graph ###
All plotly rendering happens in the function ```feature_plot```.
Make any changes to the plot there.
This is also where I update datapoint outline widths and highlight certain parts of the plot, depending on what text the user is hovering over.
Datapoint features come from ```o_points``` and ```l_points``` and outline widths come from ```o_outline_width``` and ```l_outline_width```. Look for ```fig.add_trace```.
Plot highlighting comes from ```rect_coords```. Look for ```fig.add_shape```.
Note that because the plotly uses reactive values (i.e. ```var_name.get()```), it will update automatically when ```var_name``` is changed.

### Calculations ###
All my calculations happen in helper functions, namely ```calculate_entropy```, ```calculate_condent```, ```calculate_infogain```.
Then, I have another helper function to make all of the necessary calculations, ```calculate```, which returns a dictionary called ```info``` with all the necessary numbers I need to display.
If you want to change the calculations, you can do so in these functions.

### Toggling ###
The toggling button rendering happens in ```show_toggling```.
Essentially, I have three reactive values to keep track of which toggle button was pressed (or none), and then use if-statements to render the correct text.
This requires a lot of HTML and CSS styling, and currently is somewhat hard-coded because the arrow pointing is difficult to work with.
If you wish to add/remove toggling options, do so there by make a corresponding reactive value, writing a corresponding if statement, and returning a corresponding ui.HTML.


# Design Decisions #
The goal of this visualization is to help users understand how the computations behind information gain are related to the data, so that the math is easier to understand and ideally more intuitive.

### Toggle Buttons ###
I've created toggle buttons for notation, variables, and definitions. This feature was designed for the sake of user convenience and efficiency; they can get a quick refresher on key concepts and terminology if needed, to help them follow along with the information gain calculations. There's no need to go back and review their notes or google themselves.

### Step-by-Step Calculations ###
I have a previous step and next step button for the information gain calculations, where users can go through each calculation one-by-one.
Originally, the idea was for the step-by-step to be more detailed — starting from the equation, expanding into the numerical values, and then progressing through each necessary calculation.
However, due to time constraints, all it does is hide the previous calculation/show the next calculation.

Another design choice for this feature was to show all the calculations by default so that users can easily skim through the website's visualization without having to click next over and over. This way, they can get a quick overview of the information gain calculations, especially if they're just using it as review material.

