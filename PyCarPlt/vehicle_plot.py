import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from PyCarPlt.vehicle2d import *
from PyCarPlt.vehicle2d_dual_track import *
from PyCarPlt.tire2d import *

class vehicle_plot:
    """vehicle plot in 2d
    This class is used to draw the vehicle body and tires. The vehicle body is drawn using the vehicle2d class,
    and the tires are drawn using the tire2d class.
    """

    def __init__(self, vehicle, csv_data_file=None, **kwargs):
        self.vehicle = vehicle
        self.df = pd.read_csv(csv_data_file)
        self.driver_cmd = [0, 0, 0]  # steer, accel, decel

    def update_vehicle_by_row_num(self, row_num):
        """update the vehicle pose by row number of the data file
        This current function is coupled with a specific data file format. It will be generalized in the future.
        row_num: the row number in the data
        """
        psi = self.df.iloc[row_num]['psi']
        xdot = self.df.iloc[row_num]['xdot']
        ydot = self.df.iloc[row_num]['ydot']
        F_tire_fl = [self.df.iloc[row_num]['Fx_0'], self.df.iloc[row_num]['Fy_0']]
        F_tire_fr = [self.df.iloc[row_num]['Fx_1'], self.df.iloc[row_num]['Fy_1']]
        F_tire_rl = [self.df.iloc[row_num]['Fx_2'], self.df.iloc[row_num]['Fy_2']]
        F_tire_rr = [self.df.iloc[row_num]['Fx_3'], self.df.iloc[row_num]['Fy_3']]
        slip_angle_fl = self.df.iloc[row_num]['Alpha_0']
        slip_angle_fr = self.df.iloc[row_num]['Alpha_1']
        slip_angle_rl = self.df.iloc[row_num]['Alpha_2']
        slip_angle_rr = self.df.iloc[row_num]['Alpha_3']

        self.vehicle.update_body_pose(heading=psi,vel_bframe=(xdot,ydot))
        self.vehicle.update_tire_forces(tire_forces=(F_tire_fl,F_tire_fr,F_tire_rl,F_tire_rr),\
                            slip_angles=(slip_angle_fl,slip_angle_fr,slip_angle_rl,slip_angle_rr))

    def update_vehicle_by_time(self, time):
        """update the vehicle pose by time
        time: the time in the data
        """
        # find the row number in the data file that is closest to the given time
        row_num = self.df.index[(self.df['time']-time).abs().argsort()[0]]
        self.update_vehicle_by_row_num(row_num)
    
    def update_driver_cmd(self, steer, accel, decel):
        """update the driver command
        steer: the steering angle in rad (handwheel angle)
        accel: the acceleration pedal position in [0,1]
        decel: the deceleration pedal position in [0,1]
        """
        self.driver_cmd = [steer, accel, decel]


    def update_driver_cmd_by_row_num(self, row_num):
        """update the driver command by row number of the data file
        This current function is coupled with a specific data file format. It will be generalized in the future.
        row_num: the row number in the data
        """
        steer = self.df.iloc[row_num]['Steer']
        accel = self.df.iloc[row_num]['Accel']
        decel = self.df.iloc[row_num]['Decel']
        self.update_driver_cmd(steer, accel, decel)

    def update_driver_cmd_by_time(self, time):
        """update the driver command by time
        time: the time in the data
        """
        # find the row number in the data file that is closest to the given time
        row_num = self.df.index[(self.df['time']-time).abs().argsort()[0]]
        self.update_driver_cmd_by_row_num(row_num)
