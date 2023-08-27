import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Create the figure and axes
fig, ax = plt.subplots()

# Create the scatter object
scatter = ax.scatter([], [], s=100, c='black')

# Define the function to be called on each frame
def animate(i):
    # Generate the x and y data for the current frame
    x = np.random.rand(100)
    y = np.random.rand(100)

    # Update the scatter data
    scatter.set_offsets(np.c_[x, y])

    # Set the x and y limits of the axes
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))

    return scatter,

# Create the animation object
anim = animation.FuncAnimation(fig, animate, frames=5, interval=1000, blit=True)

# Show the animation
plt.show()