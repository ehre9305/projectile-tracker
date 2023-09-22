# Projectile tracker
This is a school project that tracks a colored projectile and calculates its trajectory.
## Installation
Amusing you have a recent version of [python](https://www.python.org/downloads/) installed, you need to download this repository and run `pip install -r requirements.txt` from inside the repo
* `network-requirements.txt` is for interacting with a robot, you do not need to install from it
## Usage
`python main.py` runs the filter, which saves the points it records to `points.csv` and lines that fit those points to `coeffs.csv`
* They yellow circle is the current point, and the yellow outlines show the edges of the filtered image.
* Setting the scale - click on two points to set a reference line, and right click to set its distance in the python terminal
* Adjusting the filter - adjust the Hmin, Smin, Vmin, Hmax, Smax and Vmax trackbars to adjust the hue, saturation, and value ranges.
* Starting recording - enable by switch the active trackbar to 1, and increase the start y trackbar to lower the pink line. Once the current point is above that line and the active is 1, the program starts recording and stops when when the current point goes back bellow it.
* Adjust the scale based on the current data - press s
* Clearing the recorded data - press r
* Automatically set lines and activate - press space, the program will move the end line to the current location of the projectile and the start line 1/6 of the frame above it

`python liveplot.py` runs the plot window which monitors `points.csv` and `coeffs.csv` and graphs the points and lines when they update.
