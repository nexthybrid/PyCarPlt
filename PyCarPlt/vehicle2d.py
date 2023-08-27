import matplotlib.pyplot as plt
import math
import numpy as np
from PyCarPlt.lib_graphic import *

class vehicle2d:
    """vehicle for drawing vehicle diagram in 2d
    The vehicle CG is always assumed at the origin on the plotting axes.
    """
    wheel_base = [] # distance between front and rear axle in meter
    front_to_cg = [] # distance between front axle to cg in meter
    body_size = [] # (length,width) in meter
    tire_size = [] # (width,diameter) in meter
    heading = [] # vehicle body longitudinal axis heading in radians
    vel_bframe = [] # (vel_long_bframe,vel_lat_bframe) vehicle body velocity in body frame
    yaw_rate = [] # body yaw rate in rad/s
    
    def __init__(self,wheel_base=3.075,front_to_cg=1.392,body_size=(4.5,1.8),tire_size=(0.3,0.6),heading=math.pi/6,vel_bframe=(10,4),
                yaw_rate=0.5):
        self.wheel_base = wheel_base
        self.front_to_cg = front_to_cg
        self.body_size = body_size
        self.tire_size = tire_size
        self.heading = heading
        self.vel_bframe = vel_bframe
        self.yaw_rate = yaw_rate
        
    def draw_veh_body(self, ax = None, z_up=-1, draw_vel=True):
        """draws the body of the vehicle
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        ax: Matplotlib axis to draw on.
        draw_vel: whether to draw vehicle body velocity vector.
        NOTE: currently, vehicle center of gravity (CG) is chosen to be the origin in the drawing.
        the vehicle body box is assumed to be centered at the vehicle CG. This will be generalized in the future.
        """
        if ax is None:
            ax = plt.gca()  # Get the current axis if not provided
        
        # calculate coordinates for the vehicle body using body_size,front_to_cg, and heading
        (a,b) = self.body_size
        body_edges_default = [[a/2,a/2,-a/2,-a/2,a/2],[b/2,-b/2,-b/2,b/2,b/2]] # 2x5 matrix, one edge is repeated to close the loop
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        body_edges = np.matmul(rotation_matrix,body_edges_default) # 2x5 matrix

        # Use the plot data returned by plt.plot() to draw the vehicle body
        if z_up == 1:
            line, = ax.plot(body_edges[0], body_edges[1], 'b', linestyle="--")
        else:
            line, = ax.plot(body_edges[1], body_edges[0], 'b', linestyle="--")

        # axes=plt.gca()
        # axes.set_aspect('equal', adjustable='box')

        # draw center of gravity sign (this function may need refactoring in terms of axes)
        cg_sign(radius=0.1,ax=ax) 

        # draw yaw rate arc arrow
        if self.yaw_rate > 0:
            arc_arrow((0, 0), 0.2, 0, 180, ax=ax, linewidth=0.5, z_up=z_up)
        else:
            arc_arrow((0, 0), 0.2, 0, -180, ax=ax, linewidth=0.5, z_up=z_up)
        ax.text(0, 0.4, r"$r$", color='k', fontsize=10)

        if draw_vel:
            self.draw_veh_vel(ax=ax, z_up=z_up)
        
        return line
        
    def draw_veh_vel(self, ax = None, z_up=-1, vl_ratio=10):
        """draws the vehicle body velocity vector at the vehicle CG
        ax: Matplotlib axis to draw on.
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        vl_ratio: velocity(m/s)-length(m) ratio for determining the length of velocity arrow on figure
        
        the original velocity components are given in body frame, which needs to be transformed to global frame
        using the vehicle body heading information.
        the text annotation is placed near the head of the arrow, with a 150 degree u-turn with a length of l_text
        """
        if ax is None:
            ax = plt.gca()
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        (Vxb,Vyb) = self.vel_bframe
        Vxb_scaled = Vxb / vl_ratio
        Vyb_scaled = Vyb / vl_ratio
        V_line_default = [[0,Vxb_scaled],[0,Vyb_scaled]] # vector format 2x2 [[x1,x2],[y1,y2]], for both z-up and z-down
        V_line_rotated = np.matmul(rotation_matrix,V_line_default) # force rotated to world frame but centered at tire CG
        # draw_vector_with_text(V_line_rotated,"k",ax=ax, text=r"$V$",l_text=0.3,z_up=z_up,turn_ang=5/6*math.pi)
        draw_vector_with_text_rf(V_line_rotated, ax=ax, z_up=z_up, turn_ang=5/6*math.pi)