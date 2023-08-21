import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import seaborn as sns
from vehicle2d_single_track import *

class vehicle_stats_plot:
    """a class to create templated vehicle stats plots"""
    plot_settings = [] # some plot settings TBD
    vehicle_info = [] # () vehicle information in dictionary format
    
    def __init__(self,vehicle_info={"mass":1700,"velocity":10}):
        self.plot_settings = []
        self.vehicle_info = vehicle_info
    
    def plot_sideslip_stats(self,veh_obj):
        """plot the sideslip dynamics stats, specifically, the individual components on the RHS of betaDot
        veh_obj: the vehicle2d_single_track that provides vehicle information
        
        List of variables to plot (alternatively q1 to qN):
        delta, beta, delta-beta, Fyft*cos(delta-beta)/m_veh/V, Fxft*sin(delta-beta)/m_veh/V, Fyrt*cos(beta)/m_veh/V, -Fxrt*sin(beta)/m_veh/V
        """
        fig,ax = plt.subplots(1,1)
        
        delta = veh_obj.front_wheel_angle
        beta = math.atan2(veh_obj.vel_bframe[1],veh_obj.vel_bframe[0])
        (Fxfb,Fyfb,Fxrb,Fyrb) = veh_obj.calc_force_axles_bframe()
        Fxft=veh_obj.front_tire.longitudinal_force_tframe
        Fyft=veh_obj.front_tire.lateral_force_tframe
        Fxrt=veh_obj.rear_tire.longitudinal_force_tframe
        Fyrt=veh_obj.rear_tire.lateral_force_tframe
        m_veh = self.vehicle_info["mass"]
        V = self.vehicle_info["velocity"]
        r = veh_obj.yaw_rate
        
        q1 = delta
        q2 = beta
        q3 = delta-beta
        q4 = Fyft*math.cos(q3)/m_veh/V
        q5 = Fxft*math.sin(q3)/m_veh/V
        q6 = Fyrt*math.cos(beta)/m_veh/V
        q7 = -Fxrt*math.sin(beta)/m_veh/V
        q8 = -r
        
        df = pd.DataFrame()
        df['name'] = [r"$\delta$",r"$\beta$",r"$\delta-\beta$",r"$F_{yft}\cos{(\delta-\beta)} / mV$",
                     r"$F_{xft}\sin{(\delta-\beta)} / mV$",r"$F_{yrt}\cos{\beta} / mV$",r"$-F_{xrt}\sin(\beta) / mV$",r"$-r$"]
        df['value'] = [q1,q2,q3,q4,q5,q6,q7,q8]
        
        df2 = pd.melt(df, id_vars ='name', var_name='type of change', value_name='change in the output')
        for typ, df in zip(df2['type of change'].unique(),df2.groupby('type of change')):
            ax.barh(df[1]['name'], df[1]['change in the output'], height=0.3, label=typ)
        plt.title(r"$\dot{\beta}=\frac{F_{xft}\sin{(\delta-\beta)}+F_{yft}\cos{(\delta-\beta)}+F_{yrt}\cos{\beta}-F_{xrt}\sin(\beta)}{mV}-r$")