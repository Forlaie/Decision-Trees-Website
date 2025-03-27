A website that visualizes decision trees (ML concept)  
CSC392 project

### Installation ###
Simply git clone the repository and then run the program! (double-check)

### MathJax Equation Content ###
All MathJax equations are stored and created in the function ```create_mathjax_content```, so if you wish to change the equations or add new text, do so there.
Note that they're all written in HTML with inline CSS. Also, if you're using MathJax, in order to actually render the MathJax reactively, you *must* include
```
<script>
  updateMathJax();
</script>
```
after your ```</div>```.

### Tooltip Content ###
Tooltip texts are created using the helper function I made, ```tooltip_test```. This is because Python Shiny Express's built-in tooltip is very difficult to use (do so at the risk of your own sanity...).
To use this, inside your ```<div>```, include ```{tooltip_test(<span style="color:red">"id"</span>, "tooltip text", "display text")}```.
Then, in order to have things happen when you hover over the tooltip, you need
```
<script>
  document.getElementById(<span style="color:red>"id"</span>).addEventListener("mouseenter", function() {{
      Shiny.setInputValue(<span style="color:blue>"hovering_id"</span>, "Hovered", {{priority: "event"}});
  }});
  document.getElementById(<span style="color:red>"id"</span>).addEventListener("mouseleave", function() {{
      Shiny.setInputValue(<span style="color:blue>"hovering_id"</span>, "Not Hovered", {{priority: "event"}});
  }});
</script>
```
after your ```</div>```,
where <span style="color:red>"id"</span> should correspond to the <span style="color:red>id</span> you passed into the ```tooltip_test``` function,
and <span style="color:blue>"hovering_id"</span> corresponds to the input value being set for that item.
With this input value, you can then make functions that will perform certain actions when the text is hovered, like such
```
@reactive.effect
@reactive.event(<span style="color:blue>input.hovering</span>)
def do_stuff():
    tooltip_state = <span style="color:blue>input.hovering()</span>
    if tooltip_state == "Hovered":
        // do stuff
    else:
        // do other stuff
```
Note that each item's <span style="color:red>id</span> and <span style="color:blue>hovering_id</span> must be unique.
