import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec  # to manage subplot layout
# add the project root to the Python path so we can import the module
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from PyCarPlt.vehicle2d_dual_track import *
from PyCarPlt.vehicle_plot import *

# Set up the animation parameters
min_time = 0
max_time = 20
step = 0.1
x_min = -5
x_max = 5
y_min = -5
y_max = 5

# Create a vehicle object and a vehicle plot object
v = vehicle2d_dual_track(z_up_tire_f=1)
p = vehicle_plot(v, csv_data_file='examples/drift_data.csv')

# Create a more complex layout using gridspec
gs = gridspec.GridSpec(1, 4, width_ratios=[10, 1, 1, 1])
fig = plt.figure()
ax1 = plt.subplot(gs[0])
ax_steer = plt.subplot(gs[1])
ax_accel = plt.subplot(gs[2])
ax_decel = plt.subplot(gs[3])

ax1.set_aspect('equal')
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)

# Create an initial empty vehicle plot
initial_vehicle_plot, = ax1.plot([], [], 'b')

# Create the individual bar charts
bar_steer = ax_steer.bar("Steer", 0, color='blue')
ax_steer.set_ylim([-8, 8])
bar_accel = ax_accel.bar("Accel", 0, color='green')
ax_accel.set_ylim([0, 1])
bar_decel = ax_decel.bar("Decel", 0, color='red')
ax_decel.set_ylim([0, 1])

# Create a slider
ax_slider = plt.axes([0.25, 0.02, 0.65, 0.03])
time_slider = Slider(ax_slider, 'Time', min_time, max_time, valinit=min_time)

# Function to update the plot based on slider
def slider_update(val):
    ax1.clear()
    p.update_vehicle_by_time(val)
    p.update_driver_cmd_by_time(val)

    steer = p.driver_cmd[0]
    accel = p.driver_cmd[1]
    decel = p.driver_cmd[2]
    # (Debug) print the values to the console
    # print("Steer: ", steer, "Accel: ", accel, "Decel: ", decel)
    # (Debug) print the wheel angles to the console

    bar_steer[0].set_height(steer)
    bar_accel[0].set_height(accel)
    bar_decel[0].set_height(decel)

    # Draw vehicle and set limits
    v.draw_vehicle(ax=ax1, z_up=-1)
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)

    fig.canvas.draw_idle()

# Link the slider update function
time_slider.on_changed(slider_update)

# Show the initial frame
slider_update(min_time)

plt.show()