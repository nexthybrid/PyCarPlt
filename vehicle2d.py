import matplotlib.pyplot as plt
import math
import numpy as np

class vehicle2d:
    """vehicle for drawing vehicle diagram in 2d
    The vehicle CG is always assumed at the origin on the plotting axes.
    """
    wheel_base = [] # distance between front a rear axle in meter
    front_to_cg = [] # distance between front axle to cg in meter
    body_size = [] # (length,width) in meter
    tire_size = [] # (width,diameter) in meter
    heading = [] # vehicle body longitudinal axis heading in radians
    
    def __init__(self,wb=3.075,f2cg=1.392,bsize=(4.5,1.8),tsize=(0.3,0.6),hdng=math.pi/6):
        self.wheel_base = wb
        self.front_to_cg = f2cg
        self.body_size = bsize
        self.tire_size = tsize
        self.heading = hdng
        
    def draw_veh_body(self,z_up=-1):
        """draws the body of the vehicle
        z_up: the SAE-670 z-up (or z-down) convention for drawing. 1 for z-up, -1 for z-down
        
        vehicle center of gravity (CG) is chosen to be the origin in the drawing
        the vehicle body box is assumed to be centered at the vehicle CG
        """
        # calculate coordinates for the vehicle body using body_size,front_to_cg, and heading
        (a,b) = self.body_size
        body_edges_default = [[a/2,a/2,-a/2,-a/2,a/2],[b/2,-b/2,-b/2,b/2,b/2]] # 2x5 matrix, one edge is repeated to close the loop
        # the rotation_matrix rotates vectors in the body frame back to the world frame with an angle of -self.heading
        rotation_matrix = [[math.cos(-self.heading),math.sin(-self.heading)],
                           [-math.sin(-self.heading),math.cos(-self.heading)]] # 2x2 matrix
        body_edges = np.matmul(rotation_matrix,body_edges_default) # 2x5 matrix
        #fig = plt.figure()
        #ax = fig.add_subplot(111)
        if (z_up==1):
            plt.plot(body_edges[0], body_edges[1], 'b', linestyle="--")
        else:
            plt.plot(body_edges[1], body_edges[0], 'b', linestyle="--")
        axes=plt.gca()
        axes.set_aspect('equal', adjustable='box')