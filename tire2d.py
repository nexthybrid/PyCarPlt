import matplotlib.pyplot as plt
import math
import numpy as np
class tire2d:
    """vehicle tire in 2d"""
    tire_size = [] # meter
    longitudinal_force = [] # Newton
    lateral_force = [] # Newton
    slip_angle = [] # radian
    
    def __init__(self,tsize=(0.3,0.6),long_f=100,lat_f=1000,slip_ang=0.05):
        self.tire_size = tsize
        self.longitudinal_force = long_f
        self.lateral_force = lat_f
        self.slip_angle = slip_ang
        
    def draw_tire(self,tire_pose,z_up=-1,draw_force=1,fl_ratio=2000):
        """
        tire_pose: tuple of (x_tire,y_tire,heading_tire) in (meter,meter,radian), all in world frame
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        draw_force: whether tire forces are drawn, 1 for yes 0 for no
        fl_ratio: force(N)-length(m) ratio for determining the length of force arrow on figure
        """
        # calculate coordinates for the tire using tire_size and tire_pose
        (w,d) = self.tire_size
        (x_tire,y_tire,heading_tire) = tire_pose
        tire_edges_default = [[d/2,d/2,-d/2,-d/2,d/2],[w/2,-w/2,-w/2,w/2,w/2]] # 2x5 matrix, one edge is repeated to close the loop
        # the rotation_matrix rotates the tire frame back to the world frame with an angle of -heading_tire
        rotation_matrix = [[math.cos(-heading_tire),math.sin(-heading_tire)],
                           [-math.sin(-heading_tire),math.cos(-heading_tire)]] # 2x2 matrix
        tire_edges_rotated = np.matmul(rotation_matrix,tire_edges_default) # 2x5 matrix
        tire_edges_rotated_translated = [tire_edges_rotated[0]+x_tire,tire_edges_rotated[1]+y_tire]
        plt.plot(tire_edges_rotated_translated[0], tire_edges_rotated_translated[1], 'k', linestyle="-")
        axes=plt.gca()
        axes.set_aspect('equal', adjustable='box')
        
        if(draw_force==1):
            Fxt_scaled = self.longitudinal_force / fl_ratio
            Fyt_scaled = self.lateral_force / fl_ratio
            Fxt_line_default = [[0,Fxt_scaled],[0,0]]
            Fyt_line_default = [[0,0],[0,Fyt_scaled]]
            Fxt_line_rotated = np.matmul(rotation_matrix,Fxt_line_default)
            Fyt_line_rotated = np.matmul(rotation_matrix,Fyt_line_default)
            Fxt_line_rotated_translated = [Fxt_line_rotated[0]+x_tire,Fxt_line_rotated[1]+y_tire]
            Fyt_line_rotated_translated = [Fyt_line_rotated[0]+x_tire,Fyt_line_rotated[1]+y_tire]
            plt.plot(Fxt_line_rotated_translated[0], Fxt_line_rotated_translated[1], 'r', linestyle="-")
            plt.plot(Fyt_line_rotated_translated[0], Fyt_line_rotated_translated[1], 'g', linestyle="-")