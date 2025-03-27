### Introduction ###
A web-based visualization for Decision Tree Models, specifically the Information Gain calculation aspect (CSC311)

### Installation ###
```
git clone https://github.com/Forlaie/Decision-Trees-Website.git
pip install -r requirements.txt
cd Decision-Trees-Website
python app.py
```

### MathJax Equation Content ###
All MathJax equations are stored and created in the function ```create_mathjax_content```, so if you wish to change the equations or add new text, do so there.
Note that they're all written in HTML with inline CSS. Also, if you're using MathJax, in order to actually render the MathJax reactively, you *must* include:
```
<script>
  updateMathJax();
</script>
```
after your ```</div>```.

### Tooltip Content ###
Tooltip texts are created using the helper function I made, ```tooltip_test```. This is because Python Shiny Express's built-in tooltip is very difficult to use and customize (do so at the risk of your own sanity...).
To use this, inside your ```<div>```, include ```{tooltip_test("id", "tooltip text", "display text")}```.
Then, in order to have things happen when you hover over the tooltip, you need:
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
