A website that visualizes decision trees (ML concept)  
CSC392 project

### Installation ###
Simply git clone the repository and then run the program! (double-check)

### MathJax Equation Content ###
All MathJax equations are stored and created in the function ```create_mathjax_content```, so if you wish to change the equations or add new text, do so there.
Note that they're are written in HTML with inline CSS. Also, if you're using MathJax, in order to actually render the MathJax reactively, you *must* include
```
<script>
  updateMathJax();
</script>
```
after your ```</div>```

### Tooltip Content ###
Tooltip texts are created using the helper function I made, ```tooltip_test```
