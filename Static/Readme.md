This project was born over the course of a summer, with a lot of trial and error along the way. 
This project is a Python simulator that graphs electric charges and fields. It was born 
from a self study of Griffiths Electrodynamics, and is the start of a larger scale adaptation of the second chapter into 
Python.  

**Features:**  
Run mode 1: A basic vector field that simulates an electric charge with input from the user. 
Run mode 2:A vector field that simulates the interactions between two charges with inputs from the user, including distance between charges and 
charge strengths.        
Run mode 3: A vector field of given strength, with a gaussian sphere encircling it, and a probe point, with radius and probe point coordinates chosen by the user.
Function will return flux as well.         
Run mode 4: A purely cosmetic interpretation of a dirac delta cluster. Since dirac delta represents particles, this was an attempt to simulate it.

**Installation Guide:**                                
Python software is required, PyCharm preferred.  
Go to terminal, and input "pip install numpy scipy matplotlib"  or use "pip install -r Requirements.txt"  
After downloading requirements and simulator, run Physics.py using green play button. Prompts will appear asking you to select functions, the functions are listed above.
HTML site is in static, python file (what you run, isn't). To see screenshots, run static/Index.html and go to gallery.  

**Honest Limits:**  
The charges need to be modified so that the vector arrows scale properly, right now everything has been scaled to a base size to avoid any breaks and scaling issues at the origin, by next releases, magnitude scaling will be improved.  

**Credits:**  
Griffith's Electrodynamics Fourth Edition.  
Radu Udrea.