# -*- coding: utf-8 -*-
"""
Post processing tool for turbulent boundary layer velocity profiles from Ansys Fluent

@author: Moncef El Moatamid
date: 2022/2023
"""


"""
User guide:

    - Enter input variables in the "Input variables" section
        Enter the simulation data directory and the files names
        Enter the x coordinates of the profiles to plot in increasing order

    - Choose the profiles to plot in the "Choose Profiles to plot" section
        Write True or False to choose the profiles to plot
        Write the legend variable in the "legend_i" variable (i = 0, 1, 2, 3, 4, 5)
        Write the title of the plot in the "title_i" variable (i = 0, 1, 2, 3, 4, 5)

    - Choose the curves to plot in the "Choose curves to plot" section
        Write True or False to choose the curves to plot
    
    - Choose to print turbulence parameters in the "Print TBL properties" section
        Write True or False to choose to print the turbulence properties

"""

#####################################################################################
################################## Input variables ##################################
#####################################################################################

# Simulation data : Ansys Fluent
# # Results directory
dir = "data/"
# # Velocity profile file
profiles_file = "profiles"
# # Shear stress file
tau_file = "shear-stress"
# # Pressure gradient file
gradp_file = "dp_dx"


# Profiles' x coordinates (m) : must be in increasing order
x = [1, 2, 3, 4, 4.5, 5, 5.5, 5.7, 6, 6.2, 6.5, 6.7]

#####################################################################################
################################## Post processing ##################################
#####################################################################################

#                              Choose Profiles to plot

"""
User must choose the profiles to plot and the legend
the available variables for the legend are:
    - Re_x : reynolds = u_e*x/nu
    - Re_tau : friction reynolds = ẟ*utau/nu
    - Re_theta : momentum thickness reynolds = θ*u_e/nu
    - beta : Clauser parameter = gradp ẟ* / utau² 
    - p_plus : Mellor's pressure gradient parameter = gradp*nu/utau³
    - K : Launder's acceleration parameter = gradp nu / (rho u_e^3)
To choose the legend do : legend_i = "Re_x" (for example)
""" 

# # Velocity raw profiles u = f(y)
plot_profiles_0 = True
legend_0 = "Re_x"
title_0 = "Velocity profiles"
# # Velocity profile u/u_e = f(y/ẟ)
plot_profiles_1 = True
legend_1 = "Re_x"
title_1 = "Velocity profiles"
# # Velocity profiles u+ = f(y+)
plot_profiles_2 = True
plot_log_law = True
plot_sub_layer = True
legend_2 = "p_plus"
title_2 = "Velocity profiles"
# # Velocity profiles (u_e-u)/u_τ = f(y/ẟ)
plot_profiles_3 = True
legend_3 = "beta"
title_3 = "Velocity profiles"
# # Velocity profiles (u_e-u)/u_τ = f(y/Δ)
plot_profiles_4 = True
legend_4 = "Re_theta"
title_4 = "Velocity profiles"
# # Velocity profiles (u-u_e)/u_e = f(y/x)
plot_profiles_5 = True
legend_5 = "Re_x"
title_5 = "Velocity profiles"
# # Velocity profiles (u-u_e)/(u_e ẟ*/ẟ)=f(y/ẟ) (Zagarola Smits scaling)
plot_profiles_6 = True
legend_6 = "Re_x"
title_6 = "Velocity profiles"

#                            Choose curves to plot

# # plot Clauser parameter beta = f(x)
plot_beta = True
# # plot Launder's acceleration parameter K = f(x)
plot_K = False
# # plot Mellor's pressure gradient parameter p+ = f(x)
plot_p_plus = False

#       Print turbulent boundary layer properties at different x coordinates
print_properties = True

#####################################################################################
########################### Launch Post processing tool #############################
#####################################################################################

with open("postprocessing.py") as f:
    exec(f.read())