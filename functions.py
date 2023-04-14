# -*- coding: utf-8 -*-
"""
Useful functions for post processing turbulent boundary layer velocity profiles from Ansys Fluent

@author: Moncef El Moatamid
date: 2022/2023
"""
import numpy as np
import matplotlib.pyplot as plt
import re

#############################################################################
############################# Read Fluent files #############################
#############################################################################

def readXcste(filename, dir):
    # Read a Fluent file with multiple plots (e.g. velocity profiles at different x coordinates)
    # and return a dictionary with the x coordinates as keys and the corresponding data as values
    # code adapted from Julie's code

    with open(filename,'r') as file:
        filedata = file.read()
    Groups = re.findall('xy\/key\/label "x_(\d+)"\)\s([\s\d\-e\.]+)\)\s',filedata)
    # Groups = re.findall('xy\/key\/label "x_([\d+\.])"\)\s([\s\d\-e\.]+)\)\s',filedata)
    xValues = np.ones((len(Groups),1))
    data = {}
    for i in range(0,len(Groups)):
        xValues[i]=float(Groups[i][0])
        data[float(xValues[i])]=np.transpose(np.array([[float(j) for j in k.split('\t')] for k in Groups[i][1].splitlines()]))
    return data


def readXlist(filename, x_list):
    # Read a Fluent file at y = const and return values at the x coordinates in x_list
    file = open(filename, "r")
    lines = file.readlines()
    shear_stress = []
    x  = []
    for i in range(4,len(lines)-1):
        coord = lines[i].strip("\n").split("\t")
        x.append(float(coord[0]))
        shear_stress.append(float(coord[1]))
    sort_index = np.argsort(x)
    shear_stress, x = np.array(shear_stress), np.array(x)
    shear_stress, x = shear_stress[sort_index], x[sort_index]
    tau_list = np.interp(np.array(x_list), x, shear_stress)
    return tau_list

#############################################################################
########################## Plot velocity profiles ###########################
#############################################################################

def write_legend(x, profiles, variable):
    legend = []
    if variable == "Re_x":
        for i in range(len(x)):
            Re = profiles[i].reynolds_x()
            legend.append(f"x={x[i]}m - Re_x={Re:.1e}")
    elif variable == "Re_tau":
        for i in range(len(x)):
            Re = profiles[i].friction_reynolds()
            legend.append(f"x={x[i]}m - Re_τ={Re:.1e}")
    elif variable == "Re_theta":
        for i in range(len(x)):
            Re = profiles[i].momentum_thickness_reynolds()
            legend.append(f"x={x[i]}m - Re_θ={Re:.1e}")
    elif variable == "p_plus":
        for i in range(len(x)):
            p_plus = profiles[i].p_plus()
            legend.append(f"x={x[i]}m - p+={p_plus:.5f}")
    elif variable == "beta":
        for i in range(len(x)):
            beta = profiles[i].beta()
            legend.append(f"x={x[i]}m - β={beta:.3f}")
    elif variable == "K":
        for i in range(len(x)):
            K = profiles[i].launder_acceleration_parameter()
            legend.append(f"x={x[i]}m - K={K:.3e}")
    return legend
    

def profile_plotting(profiles, legend, title, labels, line, log_scale):
    for i, profile in enumerate(profiles):
        plt.plot(profile[0], profile[1], line[i], label=legend[i])
    plt.title(title)
    plt.ylabel(labels[1])
    plt.xlabel(labels[0])
    if log_scale:
        plt.xscale('log')
    plt.legend(fontsize = 9)
    plt.show()

def profile_plot0(profiles):
    plots = []
    for profile in profiles:
        plots.append((profile.u, profile.y))
    return plots

def profile_plot1(profiles): # u/u_e=g(y/ẟ)
    plots = []
    for profile in profiles:
        plots.append((profile.u_ue_scaling(), profile.y_delta_scaling()))
    return plots

def profile_plot2(profiles):
    plots = []
    for profile in profiles:
        plots.append((profile.y_plus(), profile.u_plus()))
    return plots

def profile_plot3(profiles): # (u-u_e)/u_τ=g(y/ẟ)
    plots = []
    for profile in profiles:
        plots.append((profile.y_delta_scaling(), profile.u_outer_scaling()))
    return plots

def profile_plot4(profiles): # Clauser Rotta scaling y/Δ : (u-u_e)/u_τ=g(y/Δ)
    plots = []
    for profile in profiles:
        plots.append((profile.y_clauser_rotta_scaling(), profile.u_outer_scaling()))
    return plots

def profile_plot5(profiles): # gradP scaling (u-u_e)/u_e=g(y/x)
    plots = []
    for profile in profiles:
        plots.append((profile.y_gradp_scaling(), profile.u_gradp_scaling()))
    return plots

def profile_plot6(profiles): # Zagarola Smits scaling (u-u_e)/(u_e ẟ*/ẟ)=g(y/ẟ)
    plots = []
    for profile in profiles:
        plots.append((profile.y_clauser_rotta_scaling(), profile.u_zagarola_smits_scaling()))
    return plots

#############################################################################
############################## Plot curves ##################################
#############################################################################

def plotting_beta(profiles, x):
    beta = [profile.beta() for profile in profiles]
    plt.scatter(x, beta)
    plt.title("Clauser's pressure gradient parameter : β")
    plt.xlabel("x [m]")
    plt.ylabel("β")
    plt.show()

def plotting_p_plus(profiles, x):
    p_plus = [profile.p_plus() for profile in profiles]
    plt.scatter(x, p_plus)
    plt.title("Pressure gradient parameter : p+")
    plt.xlabel("x [m]")
    plt.ylabel("p+")
    plt.show()

def plotting_K(profiles, x):
    K = [profile.launder_acceleration_parameter() for profile in profiles]
    plt.scatter(x, K)
    plt.title("Launder's acceleration parameter : K")
    plt.xlabel("x [m]")
    plt.ylabel("K")
    plt.show()

#############################################################################
############################## TBL properties ###############################
#############################################################################

def print_TBL_properties(profiles, x):
    print("x [m] u_e [m/s]  Re_x \t\t Re_τ \t\t Re_θ \t\t ẟ \t ẟ* \t θ \t H \t β \t p+ \t\t  K")
    for i, profile in enumerate(profiles):
        Re_x = profile.reynolds_x()
        Re_tau = profile.friction_reynolds()
        Re_theta = profile.momentum_thickness_reynolds()
        beta = profile.beta()
        p_plus = profile.p_plus()
        K = profile.launder_acceleration_parameter()
        delta = profile.boundary_thickness()
        theta = profile.momentum_thickness()
        delta_star = profile.displacement_thickness()
        H = profile.shape_factor()
        ue = profile.u_e()
        print(f"{x[i]:.2f} \t {ue:.1f} \t {Re_x:.2e} \t {Re_tau:.2e} \t {Re_theta:.2e} \t {delta:.3f} \t {delta_star:.3f} \t {theta:.3f} \t {H:.3f} \t {beta:.1f} \t {p_plus:.5f} \t {K:.3e}")