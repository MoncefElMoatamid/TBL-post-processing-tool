# -*- coding: utf-8 -*-
"""
Boundary layer profile class :
    it is assumed that the boundary layer is fully developed
    the fluid is air with :
        mu = 1.7894e-5
        rho = 1.225
    These properties must be changed if the fluid is different

    The class takes as input :
        profile : a list of two arrays [y, u]
        tau : shear stress at x
        gradp : pressure gradient at x
        x : x coordinate at which the profile is taken

    The main methods of the class are :
        u_e : free stream velocity (here u_e = max(u))
        utau : friction velocity u_τ
        y_plus : y+ = y*utau/nu
        u_plus : u+ = u/utau
        boundary_thickness : ẟ (99% of u_e)
        displacement_thickness : ẟ*
        momentum_thickness : θ
        clauser_rotta_thickness : Δ
        reynolds_x : reynolds = u_e*x/nu
        friction_reynolds : Re_τ = ẟ*utau/nu
        momentum_thickness_reynolds : Re_θ = θ*u_e/nu
        log_region : logarithmic region u+ = 1/k*log(y+)+B
        sub_region : sublayer region u+ = y+
        shape_factor : shape factor H = ẟ*/θ
        beta : beta = gradp ẟ* / utau²
        p_plus : p+ = gradp nu / utau^3
        K : K = gradp nu / (rho u_e^3)


@author: Moncef El Moatamid
date: 2022/2023
"""

import numpy as np
from math import *

class bl_profile:
    mu = 1.7894e-5
    rho = 1.225
    nu = mu/rho
    k = 0.41    
    b = 5.2

    def __init__(self, profile, tau, gradp, x):
        self.tau = tau # Shear stress at x
        self.x = x # x coordinate
        self.gradp = gradp # Pressure gradient at x
        y, u = np.array(profile[0]), np.array(profile[1]) # y, u arrays
        sort_index = np.argsort(y)
        u, y = u[sort_index], y[sort_index]
        # find max of u (= u_e here)
        max_v = max(u)
        v_frac = u/max_v
        # find index of 99% of u_e
        bl_index = 0
        while v_frac[bl_index]<0.99:
            bl_index += 1
        # assign values
        self.u = np.array(u)
        self.y = np.array(y)
        self.bl_index = bl_index
        self.max_v = max_v

    def u_e(self): # free stream velocity
        return self.max_v

    def utau(self): # friction velocity u_τ
        return np.sqrt(self.tau/self.rho)
    
    def boundary_thickness(self): # ẟ (99% of u_e)
        # y,
        return self.y[min(self.bl_index,len(self.y)-1)] # [self.bl_index]

    def reynolds_x(self): # reynolds
        return self.u_e() * self.x / self.nu

    def friction_reynolds(self): # Re_τ
        delta = self.boundary_thickness()
        return delta*self.utau()/self.nu

    ####################### Scaling inner layer #######################

    def y_plus(self): # y+
        return self.y*self.utau()/self.nu

    def u_plus(self): # u+
        return self.u/self.utau()

    def log_region(self): # modèle de paroi logarithmique
        yplus = self.y_plus()
        yplus = yplus[np.where(yplus>10)]
        yplus = yplus[np.where(yplus<1000)]
        k = self.k
        b = self.b
        return yplus, (1/k)*np.log(yplus)+b

    def sub_layer(self):
        yplus = self.y_plus()
        yplus = yplus[np.where(yplus<12)]
        return yplus, yplus

    ####################### Scaling outer layer #######################

    def u_ue_scaling(self): # u/u_e
        # u = self.u[:self.bl_index + 1]
        u = self.u
        ratio = u/self.u_e()
        return ratio
    
    def y_delta_scaling(self): # y/ẟ
        # y = self.y[:self.bl_index + 1]
        y = self.y
        delta = self.boundary_thickness()
        ratio = y/delta
        return ratio

    def displacement_thickness(self): # ẟ*
        profile = self.u/self.u_e()
        profile = profile[:self.bl_index + 1]
        y = self.y[:self.bl_index + 1]
        delta_star = np.trapz(1 - profile, y)
        return delta_star
    
    def displacement_thickness_reynolds(self): # Re_ẟ*
        return self.u_e() * self.displacement_thickness() / self.nu

    def momentum_thickness(self): # θ
        profile = self.u/self.u_e()
        profile = profile[:self.bl_index + 1]
        y = self.y[:self.bl_index + 1]
        theta = np.trapz(profile * (1 - profile), y)
        return theta

    def momentum_thickness_reynolds(self): # Re_θ
        return self.u_e() * self.momentum_thickness() / self.nu

    def shape_factor(self): # H = ẟ*/θ 
        return self.displacement_thickness() / self.momentum_thickness()

    def clauser_rotta_thickness(self): # Δ
        y = self.y[:self.bl_index + 1]
        u = self.u[:self.bl_index + 1]
        Delta = np.trapz((self.u_e() - u) / self.utau(), y)
        return Delta
    
    def y_clauser_rotta_scaling(self): # y/Δ
        # y = self.y[:self.bl_index + 1]
        y = self.y
        delta = self.clauser_rotta_thickness()
        ratio = y/delta
        return ratio

    def u_outer_scaling(self):
        # u = self.u[:self.bl_index + 1]
        u = self.u
        ratio = (self.u_e() - u) / self.utau()
        return ratio

    def u_zagarola_smits_scaling(self):
        # u = self.u[:self.bl_index + 1]
        u = self.u
        ratio = (self.u_e() - u) / (self.u_e() * self.displacement_thickness() / self.boundary_thickness())
        return ratio

    def y_gradp_scaling(self): # y/x
        return self.y/self.x

    def u_gradp_scaling(self): # (u_e - u)/u_e
        u = self.u
        ratio = (self.u_e() - u) / self.u_e()
        return ratio
    
    def beta(self): # β
        return self.gradp * self.displacement_thickness() / self.tau
    
    def p_plus(self): # p+
        return self.gradp * self.nu / self.utau()**3
    
    def launder_acceleration_parameter(self): # K
        return - self.nu * self.gradp / (self.rho * self.u_e()**3)
    


