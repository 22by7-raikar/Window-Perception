# blender-quad
Blender based Quadcopter Simulation and Visualization

Based on Prof. Nitin Sanket's work
https://umdausfire.github.io/teaching/fire298/asn3.html

`main.py` This function runs the animation to visualize the path taken by the drone.  
`rrt.py` This code finds the optimal path between the goal and start.  

1. Clone the code in your PC.
2. Give the map you want to explore.
3. Run the rrt.py to find the optimal path, the rrt.py stores the values of the way points in a csv file.
4. Run the main.py, which calls the stored csv file and renders the animation of the drone following the quintic trajectory.
# Results

Plot of orientation angles estimated from all functions are plotted with legend. <br />
Please refer to `Report.pdf` for our results and methodology

