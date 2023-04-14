# -*- coding: utf-8 -*-
"""
Post processing script for turbulent boundary layer velocity profiles from Ansys Fluent

@author: Moncef El Moatamid
date: 2022/2023
"""

from boundary_layer import bl_profile
from functions import *
import sys
import matplotlib.pyplot as plt


print("################################################################################")
print("################# Fluent Boundary layer Post processing tool ###################")
print("################################################################################")

################################################################################
############################# Recover user input ###############################
################################################################################

# Read profiles file
profiles_dict = readXcste(dir + profiles_file, dir)
if len(profiles_dict) != len(x):
    print("Error: number of profiles imported is not the same as the number of x")
    sys.exit()

# wall shear stress and pressure gradient lists 
tau_w = readXlist(dir + tau_file, x)
gradp = readXlist(dir + gradp_file, x)
print("\t\t\t Fluent files imported and read")

# velocity profiles
profiles_list = [] # List of profiles objects (class "bl_profile")
x_profile = list(profiles_dict)
for i in range(len(profiles_dict)):
    y = profiles_dict[x_profile[i]][0]
    u = profiles_dict[x_profile[i]][1]
    profiles_list.append(bl_profile([y, u], tau_w[i], gradp[i], x[i]))
print("\t   Velocity profiles created with the class \"bl_profile\"")
# profile_sansgrad = bl_profile("grad=0", 3.49958, 0, 6, 0)

################################################################################
############################# Postprocessing plots #############################
################################################################################
print("\t\t\t   Start post processing\n\n")
print("\t\t\t\t\t\t Turbulent boundary layer properties:\n")
# # print TBL properties
if print_properties:
    print_TBL_properties(profiles_list, x)

# # Plot velocity profiles depending on the user input
if plot_profiles_0:
    profiles = profile_plot0(profiles_list)
    legend = write_legend(x, profiles_list, legend_0)
    lines = ["-" for i in range(len(x))]
    labels = ["u [m/s]", "y [m]"]
    log_scale = False
    profile_plotting(profiles, legend, title_0, labels, lines, log_scale)
if plot_profiles_1:
    profiles = profile_plot1(profiles_list)
    legend = write_legend(x, profiles_list, legend_1)
    lines = ["-" for i in range(len(x))]
    labels = ["u/u_e", "y/delta"]
    log_scale = False
    profile_plotting(profiles, legend, title_1, labels, lines, log_scale)
if plot_profiles_2:
    yplus_log, u_log = profiles_list[0].log_region()
    yplus_lam, u_lam = profiles_list[0].sub_layer()
    profiles = profile_plot2(profiles_list)
    legend = write_legend(x, profiles_list, legend_2)
    lines = ["-" for i in range(len(x))]
    if plot_log_law:
        profiles = profiles + [(yplus_log, u_log)]
        legend = legend + ["Log-law"]
        lines = lines + ["--"]
    if plot_sub_layer:
        profiles = profiles + [(yplus_lam, u_lam)]
        legend = legend + ["U+ = y+"]
        lines = lines + ["--"]
    labels = ["y+", "u+"]
    log_scale = True
    profile_plotting(profiles, legend, title_2, labels, lines, log_scale)
if plot_profiles_3:
    profiles = profile_plot3(profiles_list)
    legend = write_legend(x, profiles_list, legend_3)
    lines = ["-" for i in range(len(x))]
    labels = ["y/delta", "(ue-u)/u_tau"]
    log_scale = False
    profile_plotting(profiles, legend, title_3, labels, lines, log_scale)
if plot_profiles_4:
    profiles = profile_plot4(profiles_list)
    legend = write_legend(x, profiles_list, legend_4)
    lines = ["-" for i in range(len(x))]
    labels = ["y/Delta", "(u_e-u)/u_tau"]
    log_scale = False
    profile_plotting(profiles, legend, title_4, labels, lines, log_scale)
if plot_profiles_5:
    profiles = profile_plot5(profiles_list)
    legend = write_legend(x, profiles_list, legend_5)
    lines = ["-" for i in range(len(x))]
    labels = ["y/x", "(u-u_e)/u_e"]
    log_scale = False
    profile_plotting(profiles, legend, title_5, labels, lines, log_scale)
if plot_profiles_6:
    profiles = profile_plot6(profiles_list)
    legend = write_legend(x, profiles_list, legend_6)
    lines = ["-" for i in range(len(x))]
    labels = ["y/delta", "(u-u_e)/(u_e delta*/delta)"]
    log_scale = False
    profile_plotting(profiles, legend, title_6, labels, lines, log_scale)



# # Plot curves depending on the user input
if plot_beta:
    plotting_beta(profiles_list, x)
if plot_p_plus:
    plotting_p_plus(profiles_list, x)
if plot_K:
    plotting_K(profiles_list, x)

print("\n\n \t\t Post processing finished !\n\n")