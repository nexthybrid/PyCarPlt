import matplotlib.pyplot as plt
import math
import numpy as np
from vehicle2d import *
from tire2d import *
class vehicle2d_single_track(vehicle2d):
    """single track vehicle (one tire per axle)"""
    front_tire = []
    rear_tire = []
    front_wheel_angle = [] # radians
    
    def __init__(self, long_f_frnt=100, lat_f_frnt = 1000, slip_ang_frnt=0.05, whl_ang_frnt = 0, long_f_rear = 3000, lat_f_rear=1000):
        super(vehicle2d_single_track, self).__init__() # use default initialization from parent class
        self.front_tire = tire2d(self.tire_size,long_f_frnt,lat_f_frnt,slip_ang_frnt)
        self.rear_tire = tire2d(self.tire_size,long_f_rear,lat_f_rear,0)
        self.front_wheel_angle = whl_ang_frnt
        
    def draw_vehicle(self,z_up=-1,save_fig=0,fig_name='vehicle_plot.eps'):
        """draws the vehicle body and tires
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        save_fig: whether to save figure
        """
        self.draw_veh_body(z_up=z_up)
        # calculate the tires' poses
        a = self.front_to_cg
        b = self.wheel_base - self.front_to_cg
        tires_center_bframe = [[a,-b],[0,0]] # in body frame, 2x2 matrix
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        tires_center = np.matmul(rotation_matrix,tires_center_bframe) # 2x2 matrix
        tires_headings_bframe = np.array([self.front_wheel_angle,0]) # assume rear wheel is always alined with body axis
        tires_headings = tires_headings_bframe + self.heading # 2x1 matrix
        tire_pose_front = (tires_center[0,0],tires_center[1,0],tires_headings[0])
        tire_pose_rear = (tires_center[0,1],tires_center[1,1],tires_headings[1])
        self.front_tire.draw_tire(tire_pose_front,z_up=z_up)
        self.rear_tire.draw_tire(tire_pose_rear,z_up=z_up)
        plt.plot()
        if (save_fig==1):
            plt.savefig(fig_name,format='eps')