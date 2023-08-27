import matplotlib.pyplot as plt
import math
import numpy as np
from PyCarPlt.lib_graphic import *

class tire2d:
    """vehicle tire in 2d
    The tire contour and forces drawings are first rotated by the tire heading, then translated by
    tire center coordinates in global frame. Bothe tire heading and tire center coordinates are 
    provided externally (e.g. provided in a vehicle2d_single_track class member function draw_vehicle)
    """
    tire_size = [] # meter
    longitudinal_force_tframe = [] # Newton
    lateral_force_tframe = [] # Newton
    slip_angle = [] # radian
    
    def __init__(self,tsize=(0.3,0.6),long_f_tframe=100,lat_f_tframe=1000,slip_ang=0.05):
        self.tire_size = tsize
        self.longitudinal_force_tframe = long_f_tframe
        self.lateral_force_tframe = lat_f_tframe
        self.slip_angle = slip_ang
    
    def update_tire_force(self,f_tframe,slip_ang):
        """update the tire force
        f_tframe: the tire force in tire frame, 2x1 matrix [[longitudinal force],[lateral force]]
        slip_ang: the slip angle in radian
        """
        self.longitudinal_force_tframe = f_tframe[0]
        self.lateral_force_tframe = f_tframe[1]
        self.slip_angle = slip_ang
        

    def draw_tire(self, ax=None, tire_pose=None, z_up=-1, draw_force=True, draw_x_axis=True, fl_ratio=2000):
        """
        Draws the tire.
        
        ax: Matplotlib axis to draw on.
        tire_pose: Tuple of (x_tire, y_tire, heading_tire) in (meter, meter, radian), all in world frame.
        z_up: The z-up (or z-down) convention for drawing (1 for z-up, -1 for z-down).
        draw_force: Whether tire forces are drawn (True for yes, False for no).
        fl_ratio: Force (N)-length (m) ratio for determining the length of force arrow on figure.
        """
        if ax is None:
            ax = plt.gca()

        if tire_pose is None:
            tire_pose = (0, 0, 0)  # Default tire pose if not provided

        (w, d) = self.tire_size
        (x_tire, y_tire, heading_tire) = tire_pose
        tire_edges_default = [[d / 2, d / 2, -d / 2, -d / 2, d / 2],
                            [w / 2, -w / 2, -w / 2, w / 2, w / 2]]
        rotation_matrix = [[math.cos(-heading_tire), math.sin(-heading_tire)],
                        [-math.sin(-heading_tire), math.cos(-heading_tire)]]
        tire_edges_rotated = np.matmul(rotation_matrix, tire_edges_default)
        tire_edges_rotated_translated = [tire_edges_rotated[0] + x_tire, tire_edges_rotated[1] + y_tire]

        if z_up == 1:
            ax.plot(tire_edges_rotated_translated[0], tire_edges_rotated_translated[1], 'k', linestyle="-")
        else:
            ax.plot(tire_edges_rotated_translated[1], tire_edges_rotated_translated[0], 'k', linestyle="-")

        # axes = plt.gca()
        ax.set_aspect('equal', adjustable='box')

        if draw_force:
            self.draw_tire_force(ax=ax, tire_pose=tire_pose,fl_ratio=fl_ratio,z_up=z_up)
        if draw_x_axis:
            self.draw_tire_x_axis(ax=ax, tire_pose=tire_pose, z_up=z_up)


    def draw_tire_force(self, ax=None, tire_pose=None, fl_ratio=2000, z_up=-1):
        """
        Draws the tire force on top of the tire CG.
        
        ax: Matplotlib axis to draw on.
        tire_pose: Tuple of (x_tire, y_tire, heading_tire) in (meter, meter, radian), all in the world frame.
        fl_ratio: Force (N)-length (m) ratio for determining the length of force arrow on the figure.
        z_up: The z-up (or z-down) convention for drawing (1 for z-up, -1 for z-down).
        """
        if ax is None:
            ax = plt.gca()

        if tire_pose is None:
            tire_pose = (0, 0, 0)  # Default tire pose if not provided

        (x_tire, y_tire, heading_tire) = tire_pose
        rotation_matrix = [[math.cos(-heading_tire), math.sin(-heading_tire)],
                        [-math.sin(-heading_tire), math.cos(-heading_tire)]]

        Fxt_scaled = self.longitudinal_force_tframe / fl_ratio
        Fyt_scaled = self.lateral_force_tframe / fl_ratio
        Fxt_line_default = [[0, Fxt_scaled], [0, 0]]
        Fyt_line_default = [[0, 0], [0, Fyt_scaled]]

        Fxt_line_rotated = np.matmul(rotation_matrix, Fxt_line_default)
        Fyt_line_rotated = np.matmul(rotation_matrix, Fyt_line_default)

        Fxt_line_rotated_translated = [Fxt_line_rotated[0] + x_tire, Fxt_line_rotated[1] + y_tire]
        Fyt_line_rotated_translated = [Fyt_line_rotated[0] + x_tire, Fyt_line_rotated[1] + y_tire]

        if z_up == 1:
            ax.arrow(Fxt_line_rotated_translated[0][0], Fxt_line_rotated_translated[1][0],
                    Fxt_line_rotated_translated[0][1] - Fxt_line_rotated_translated[0][0],
                    Fxt_line_rotated_translated[1][1] - Fxt_line_rotated_translated[1][0], width=0.01,
                    head_width=0.05, head_length=0.1, length_includes_head=True, edgecolor='r', facecolor='r')

            ax.arrow(Fyt_line_rotated_translated[0][0], Fyt_line_rotated_translated[1][0],
                    Fyt_line_rotated_translated[0][1] - Fyt_line_rotated_translated[0][0],
                    Fyt_line_rotated_translated[1][1] - Fyt_line_rotated_translated[1][0], width=0.01,
                    head_width=0.05, head_length=0.1, length_includes_head=True, edgecolor='g', facecolor='g')
        else:
            ax.arrow(Fxt_line_rotated_translated[1][0], Fxt_line_rotated_translated[0][0],
                    Fxt_line_rotated_translated[1][1] - Fxt_line_rotated_translated[1][0],
                    Fxt_line_rotated_translated[0][1] - Fxt_line_rotated_translated[0][0], width=0.01,
                    head_width=0.05, head_length=0.1, length_includes_head=True, edgecolor='r', facecolor='r')

            ax.arrow(Fyt_line_rotated_translated[1][0], Fyt_line_rotated_translated[0][0],
                    Fyt_line_rotated_translated[1][1] - Fyt_line_rotated_translated[1][0],
                    Fyt_line_rotated_translated[0][1] - Fyt_line_rotated_translated[0][0], width=0.01,
                    head_width=0.05, head_length=0.1, length_includes_head=True, edgecolor='g', facecolor='g')


    def draw_tire_x_axis(self, ax=None, tire_pose=None, dash_length=2, z_up=-1):
        """
        Draws a black dashed line along the tire frame x axis.
        
        ax: Matplotlib axis to draw on.
        tire_pose: Tuple of (x_tire, y_tire, heading_tire) in (meter, meter, radian), all in world frame.
        dash_length: The length of the dashed line.
        z_up: The z-up (or z-down) convention for drawing (1 for z-up, -1 for z-down).
        """
        if ax is None:
            ax = plt.gca()

        if tire_pose is None:
            tire_pose = (0, 0, 0)  # Default tire pose if not provided

        (x_tire, y_tire, heading_tire) = tire_pose

        x_edge_1 = x_tire + 0.5 * dash_length * math.cos(heading_tire)
        x_edge_2 = x_tire - 0.5 * dash_length * math.cos(heading_tire)
        y_edge_1 = y_tire + 0.5 * dash_length * math.sin(heading_tire)
        y_edge_2 = y_tire - 0.5 * dash_length * math.sin(heading_tire)

        if z_up == 1:
            ax.plot([x_edge_1, x_edge_2], [y_edge_1, y_edge_2], 'k--', linewidth=0.5)
        else:
            ax.plot([y_edge_1, y_edge_2], [x_edge_1, x_edge_2], 'k--', linewidth=0.5)
