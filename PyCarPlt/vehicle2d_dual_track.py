import matplotlib.pyplot as plt
import math
import numpy as np
from PyCarPlt.vehicle2d import *
from PyCarPlt.tire2d import *


class vehicle2d_dual_track(vehicle2d):
    """dual track vehicle (two tires per axle)"""
    # fl_tire = []
    # fr_tire = []
    # rl_tire = []
    # rr_tire = []
    # wheel_angles = [] # radians
    # wheel_velocities = [] # wheel veolcoties in body frame coordinates
    
    def __init__(self, z_up_tire_f=1, **kwargs):
        super(vehicle2d_dual_track, self).__init__(**kwargs) # use default initialization from parent class
        tire_f_tframe = ((500,500),(500,500),(500,500),(500,500)) # default tire force in tire frame
        slip_angles = (0.05,0.05,0.05,0.05) # default slip angles
        self.fl_tire = tire2d(self.tire_size,tire_f_tframe[0][0],tire_f_tframe[0][1],slip_angles[0],z_up_tire_f=z_up_tire_f)
        self.fr_tire = tire2d(self.tire_size,tire_f_tframe[1][0],tire_f_tframe[1][1],slip_angles[1],z_up_tire_f=z_up_tire_f)
        self.rl_tire = tire2d(self.tire_size,tire_f_tframe[2][0],tire_f_tframe[2][1],slip_angles[2],z_up_tire_f=z_up_tire_f)
        self.rr_tire = tire2d(self.tire_size,tire_f_tframe[3][0],tire_f_tframe[3][1],slip_angles[3],z_up_tire_f=z_up_tire_f)

        self.wheel_angles = (0,0,0,0) # default wheel angles
        self.vel_front_bframe = (0,0) # default front axle velocity in body frame
        self.vel_rear_bframe = (0,0) # default rear axle velocity in body frame
        self.wheel_velocities = ((0,0),(0,0),(0,0),(0,0)) # default wheel velocities
        self.track_widths = (1.5,1.5) # default front/rear track widths

        self.z_up_tire_force = z_up_tire_f # default z-up or z-down for tire force drawing
    
    def update_body_pose(self,heading,vel_bframe):
        """update the body pose
        heading: the heading angle in radians
        vel_bframe: the body velocity in body frame
        """
        self.heading = heading
        self.vel_bframe = vel_bframe
    
    def update_wheel_angles(self, wheel_angles):
        """update the wheel angles
        wheel_angles: the wheel angles in radians
        """
        self.wheel_angles = wheel_angles
    
    def update_tire_forces(self,tire_forces,slip_angles):
        """update the tire forces
        tire_forces: the tire forces in tire frame, 4x2 matrix [[fl_longitudinal_force,fl_lateral_force],
                                                                [fr_longitudinal_force,fr_lateral_force],
                                                                [rl_longitudinal_force,rl_lateral_force],
                                                                [rr_longitudinal_force,rr_lateral_force]]
        slip_angles: the slip angles in radian, 4x1 matrix [fl_slip_angle,fr_slip_angle,rl_slip_angle,rr_slip_angle]
        """
        self.fl_tire.update_tire_force(tire_forces[0],slip_angles[0])
        self.fr_tire.update_tire_force(tire_forces[1],slip_angles[1])
        self.rl_tire.update_tire_force(tire_forces[2],slip_angles[2])
        self.rr_tire.update_tire_force(tire_forces[3],slip_angles[3])
    
    def draw_vehicle(self,ax=None, z_up=-1,save_fig=False,fig_name='vehicle_plot.eps',draw_front_tire_force=True,draw_rear_tire_force=True,
                    draw_whl_v = False):
        """draws the vehicle body and tires
        ax: Matplotlib axis to draw on.
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        save_fig: whether to save figure
        """
        if ax is None:
            ax = plt.gca()

        self.draw_veh_body(ax=ax, z_up=z_up)
        # calculate the tires' poses
        tires_center = self.calc_tires_centers()
        tires_wheel_angles_bframe = np.array(self.wheel_angles) # assume rear wheel is always alined with body axis
        tires_headings = tires_wheel_angles_bframe + self.heading # 2x1 matrix
        tire_pose_fl = (tires_center[0,0],tires_center[1,0],tires_headings[0])
        tire_pose_fr = (tires_center[0,1],tires_center[1,1],tires_headings[1])
        tire_pose_rl = (tires_center[0,2],tires_center[1,2],tires_headings[2])
        tire_pose_rr = (tires_center[0,3],tires_center[1,3],tires_headings[3])
        self.update_axle_velocity() # use body velocity, yawrate, and steer angle to calculate axle velocity
        if draw_whl_v:
            self.draw_wheel_velocity(ax=ax, z_up=z_up)
        self.fl_tire.draw_tire(ax=ax,tire_pose=tire_pose_fl,z_up=z_up,draw_force=draw_front_tire_force)
        self.fr_tire.draw_tire(ax=ax,tire_pose=tire_pose_fr,z_up=z_up,draw_force=draw_front_tire_force)
        self.rl_tire.draw_tire(ax=ax,tire_pose=tire_pose_rl,z_up=z_up,draw_force=draw_rear_tire_force)
        self.rr_tire.draw_tire(ax=ax,tire_pose=tire_pose_rr,z_up=z_up,draw_force=draw_rear_tire_force)
        # plt.plot()
        # if (save_fig):
        #     plt.savefig(fig_name,format='eps')

        return ax
            
    def calc_axles_center(self):
        """calculate the front and rear axle geometric center"""
        a = self.front_to_cg
        b = self.wheel_base - self.front_to_cg
        axles_center_bframe = [[a,-b],[0,0]] # in body frame, 2x2 matrix, assuming vehicle originally aligns with x axis
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        axles_center = np.matmul(rotation_matrix,axles_center_bframe) # 2x2 matrix ([[axle_f_x,axle_r_x],[axle_f_y,axle_r_y])
        return axles_center
    
    def calc_tires_centers(self):
        """calculate the tires' geometric centers"""
        a = self.front_to_cg
        b = self.wheel_base - self.front_to_cg
        axles_center_bframe = [[a,-b],[0,0]] # in body frame, 2x2 matrix, assuming vehicle originally aligns with x axis
        # The tires follow the fl, fr, rl, rr order
        tires_center_bframe = [[a,a,-b,-b],[self.track_widths[0]/2,-self.track_widths[0]/2,
                                            -self.track_widths[1]/2,self.track_widths[1]/2]] # in body frame, 2x4 matrix
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        tires_centers_global = np.matmul(rotation_matrix,tires_center_bframe) # 2x4 matrix 
        return tires_centers_global
            
    def calc_vel_axles_bframe(self):
        """calculate the front and rear axle velocity in body frame
        Vxfb = Vxrb = Vxb, Vyfb = Vyb + r*a, Vyrb = Vyb - r*b (valid for both z-up and z-down)
        output:
        vel_axle_bframe (Vxfb,Vyfb,Vxrb,Vyrb) tuple
        """
        Vxfb = self.vel_bframe[0]
        Vyfb = self.vel_bframe[1]+self.yaw_rate*self.front_to_cg
        Vxrb = self.vel_bframe[0]
        Vyrb = self.vel_bframe[1]-self.yaw_rate*(self.wheel_base-self.front_to_cg)
        return (Vxfb,Vyfb,Vxrb,Vyrb)
    
    def calc_force_axles_bframe(self):
        """calculate the front and rear axle forces in body frame
        This is performed by transforming the tire frame tire forces into body frame
        output:
        force_axle_bframe (Fxfb,Fyfb,Fxrb,Fyrb) tuple
        
        Here it is assumed that the tire frame and the body frame are either both z-up or both z-down
        """
        # list the tire forces
        Fxft=self.front_tire.longitudinal_force_tframe
        Fyft=self.front_tire.lateral_force_tframe
        Fxrt=self.rear_tire.longitudinal_force_tframe
        Fyrt=self.rear_tire.lateral_force_tframe
        # the rotation_matrix rotates vectors in the front tire frame back to the body frame with an angle of -self.front_wheel_angle
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        Fft = [[Fxft],[Fyft]] # 2x1 array
        Ffb = np.matmul(rotation_matrix,Fft) # matrix multiply
        Fxfb = Ffb[0]
        Fyfb = Ffb[1]
        Fxrb = Fxrt
        Fyrb = Fyrt
        # make result into 4-tuple
        return (Fxfb,Fyfb,Fxrb,Fyrb)
    
    def update_axle_velocity(self):
        """use body velocity, yawrate, and steer angle to calculate axle velocity"""
        (Vxfb,Vyfb,Vxrb,Vyrb) = self.calc_vel_axles_bframe()
        self.vel_front_bframe = (Vxfb,Vyfb)
        self.vel_rear_bframe = (Vxrb,Vyrb)
    
    def draw_wheel_velocity(self,ax= None, z_up=-1,vlratio=10):
        """
        ax: Matplotlib axis to draw on.
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        vl_ratio: velocity(m/s)-length(m) ratio for determining the length of velocity arrow on figure
        
        the wheel velocity in body frame is first rotated to the global frame, then translated
        to the axle/wheel center (currently only the front wheel velocity is implemented)
        """
        (Vxfb,Vyfb) = self.vel_front_bframe
        Vxfb_scaled = Vxfb / vlratio
        Vyfb_scaled = Vyfb / vlratio
        Vf_line_default = [[0,Vxfb_scaled],[0,Vyfb_scaled]] # vector format 2x2 [[x1,x2],[y1,y2]], for both z-up and z-down
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        Vf_line_rotated = np.matmul(rotation_matrix,Vf_line_default) # force rotated to world frame but centered at tire CG
        axles_center = self.calc_axles_center() # 2x2 matrix ([[axle_f_x,axle_r_x],[axle_f_y,axle_r_y])
        Vf_line_rotated_translated = [Vf_line_rotated[0]+axles_center[0][0],Vf_line_rotated[1]+axles_center[1][0]] # translate vector to axle/wheel center
        # draw_vector_with_text(Vf_line_rotated_translated,"k",text=r"$V_f$",l_text=0.3,z_up=z_up,turn_ang=5/6*math.pi)
        draw_vector_with_text_rf(Vf_line_rotated_translated, ax=ax, z_up=z_up, turn_ang=5/6*math.pi)
        