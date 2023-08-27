import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from vehicle2d_dual_track import *
from vehicle_plot import *

# Set up the animation parameters
min_time = 0
max_time = 20
step = 0.1
x_min = -5
x_max = 5
y_min = -5
y_max = 5

# Create a vehicle object and a vehicle plot object
v = vehicle2d_dual_track()
p = vehicle_plot(v, csv_data_file='drift_data.csv')

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_aspect('equal')  # Set aspect ratio to maintain proper scaling
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Create an initial empty vehicle plot
initial_vehicle_plot, = ax.plot([], [], 'b')

# Create a slider
ax_slider = plt.axes([0.25, 0.02, 0.65, 0.03])
time_slider = Slider(ax_slider, 'Time', min_time, max_time, valinit=min_time)

# Function to update the plot based on slider
def slider_update(val):
    ax.clear()
    p.update_vehicle_by_time(val)
    # v.draw_veh_body(ax=ax, z_up=-1)
    v.draw_vehicle(ax=ax, z_up=-1)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    fig.canvas.draw_idle()

# Link the slider update function
time_slider.on_changed(slider_update)

# Show the initial frame
slider_update(min_time)

plt.show()