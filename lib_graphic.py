# graphics library for plotting
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import numpy as np

# filled arc sector, inspired by https://stackoverflow.com/questions/30642391/how-to-draw-a-filled-arc-in-matplotlib
def arc_sector(center, radius, theta1, theta2, ax=None, resolution=50, **kwargs):
    # make sure ax is not empty
    if ax is None:
        ax = plt.gca()
    # generate the points
    theta = np.linspace(np.radians(theta1), np.radians(theta2), resolution) # 1xresolution row vector
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1])) # 2xresolution matrix
    points = np.concatenate((points, np.array([[center[0],center[1]]]).T), axis=1) # add center to the points array
    # build the polygon and add it to the axes
    poly = mpatches.Polygon(points.T, closed=True, **kwargs)
    ax.add_patch(poly)
    return poly

# the center of gravity sign
def cg_sign(radius=1,ax=None,linewidth=0.5):
    # make sure ax is not empty
    if ax is None:
        ax = plt.gca()
    circle = plt.Circle((0, 0), radius,facecolor=(1,1,1,0),edgecolor="black",linewidth=linewidth)
    ax.add_patch(circle)
    ax.plot(0,0,'k')
    arc_sector((0,0), radius, 90, 180,ax=ax, fill=True, color='black')
    arc_sector((0,0), radius, 270, 360,ax=ax, fill=True, color='black')
    ax.set_aspect('equal', adjustable='box')
    
# arc with an arrow end
def arc_arrow(center, radius, theta1, theta2, ax=None, res=50,z_up=1, **kwargs):
    # make sure ax is not empty
    if ax is None:
        ax = plt.gca()
    # generate the points
    theta = np.linspace(np.radians(theta1), np.radians(theta2), res) # 1xresolution row vector
    points = np.vstack((radius*np.cos(theta) + center[0], 
                        radius*np.sin(theta) + center[1])) # 2xresolution matrix
    
    if (z_up==1):
        ax.plot(points[0],points[1],'k',**kwargs) # plot the arc
        # plot the arrow at the end
        plt.arrow(points[0][-2],points[1][-2],points[0][-1]-points[0][-2],points[1][-1]-points[1][-2],width=0.001,
                 head_width=0.05,head_length=0.1,length_includes_head=False,edgecolor='k',facecolor='k')
    else:
        ax.plot(points[1],points[0],'k',**kwargs)
        plt.arrow(points[1][-2],points[0][-2],points[1][-1]-points[1][-2],points[0][-1]-points[0][-2],width=0.001,
                  head_width=0.05,head_length=0.1,length_includes_head=False,edgecolor='k',facecolor='k')

    
    
#     tail_coords = center[0]+radius*math.cos(theta1), center[1]+radius*math.sin(theta1)
#     head_coords = center[0]+radius*math.cos(theta2), center[1]+radius*math.sin(theta2)

    
#     connection_style = mpatches.ConnectionStyle.Arc3(rad=1) 
#     # see https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ConnectionStyle.html#matplotlib.patches.ConnectionStyle
#     style = "Simple, tail_width=0.5, head_width=4, head_length=8"
#     arrow = mpatches.FancyArrowPatch(tail_coords, head_coords,arrowstyle=style,
#                              connectionstyle=connection_style)
#     ax.add_patch(arrow)

def draw_vector_with_text(vector,color,text=r"$V$",l_text=0.3,z_up=-1,turn_ang=5/6*math.pi):
    """draw a vector with an arrow and a text near the head of the arrow
    vector: 2x2 array of [[x1,x2],[y1,y2]]
    color: color for the arrow and text, consistent
    text: text to add near the head of the arrow, located at a length of l_text after a 150-degree u-turn
    l_text: length of travel after a sharp 150-degree u-turn at the arrow head
    turn_ang: u-turn angle, default at 150 degrees.
    """
    # make sure ax is not empty
#     if ax is None:
#         ax = plt.gca()
    if (z_up==1):
        plt.arrow(vector[0][0],vector[1][0],
                 vector[0][1]-vector[0][0],
                  vector[1][1]-vector[1][0],width=0.01,
                 head_width=0.05,head_length=0.1,length_includes_head=True,edgecolor=color,facecolor=color)
        # write the symbol V half way along the vector with a slight shift
        axes=plt.gca()
        arrow_angle = np.arctan2(vector[1][1]-vector[1][0],
                                vector[0][1]-vector[0][0]) # syntax: arctan2(y,x)
        axes.text(vector[0][1]+l_text*math.cos(arrow_angle+turn_ang),
                  vector[1][1]+l_text*math.sin(arrow_angle+turn_ang), r"$V$", color=color, fontsize=10)
    else:
        plt.arrow(vector[1][0],vector[0][0],
                 vector[1][1]-vector[1][0],
                  vector[0][1]-vector[0][0],width=0.01,
                 head_width=0.05,head_length=0.1,length_includes_head=True,edgecolor=color,facecolor=color)
        axes=plt.gca()
        arrow_angle = np.arctan2(vector[1][1]-vector[1][0],
                                vector[0][1]-vector[0][0]) # syntax: arctan2(y,x)
        axes.text(vector[1][1]+l_text*math.cos(arrow_angle+turn_ang),
                  vector[0][1]+l_text*math.sin(arrow_angle+turn_ang), text, color=color, fontsize=10)