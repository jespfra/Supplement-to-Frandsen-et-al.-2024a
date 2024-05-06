# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:07:39 2023

@author: jespfra
A module that contains a plot function, a plot initiator and all the function calls to generate plots to the batch benchmarks

"""
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np


def plot_convergence(CADETFVdata,CADETJuliadata,CADETDGdata=[],profileData=[],saveLocation="",type="LRM"):
    
    colorFV = 'deeppink'
    colorDG_exact = plt.cm.Blues(range(230, 90, -30))   # Nuances of red
    colorDG_inexact =  plt.cm.Reds(range(255, 90, -40))  # Nuances of red
    colorDGJulia_exact = plt.cm.Greens(range(230, 90, -30))   # Nuances of red
    colorDGJulia_inexact =  plt.cm.Purples(range(255, 90, -30))  # Nuances of red
    colors_profile1 = ['g','r','b']
    colors_profile2 = ['m', 'c', 'y']
    markersize = 12

    if type == "GRM":
        tag = "polyDegPoreu"
        plottag = "$N_d^p$"
    else:
        tag = "polyDegu"
        plottag = "$N_d^b$"
        
    # If the case is no_binding:
    if CADETFVdata.empty and profileData.empty:
        
        # DOF MaxE plot
        fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_m1"][idx],'.--', label = f'CADET-Julia, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])

        
        # Plot CADET-DG 
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])


        ax.set_xlabel('Degrees of freedom', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend()
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.4)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_convergence.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
        
        
        # DOF Rutime plot
        fig,ax = plt.subplots(figsize=(11.5, 10))
        
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_m1"][idx],'.--', label = f'CADET-Julia, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
            
            
        # Plot CADET-DG 
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i"][idx],'-', label = f'CADET-DG, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
                
        ax.set_xlabel('Degrees of freedom', fontsize=25)
        ax.set_ylabel('Simulation time (s)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.45)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_runtime.svg'),format = 'svg',dpi = 1200)
        
        
        # Runtime Error plot
        fig,ax = plt.subplots(figsize=(11.5, 10))

        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            ax.loglog(CADETJuliadata['runtime_m1'][idx],CADETJuliadata["maxE_m1"][idx],'.--', label = f'CADET-Julia, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])

            
        # Plot CADET-DG 
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax.loglog(CADETDGdata['runtime_e'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
                
       
        ax.set_xlabel('Simulation time (s)', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.4)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_err_runtime.svg'),format = 'svg',dpi = 1200)
        
        return 
        
        
        
    
    fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
    ax.loglog(CADETFVdata['DOF'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    
    # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i] )

    
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])


    ax.set_xlabel('Degrees of freedom', fontsize=25)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend()
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.4)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_convergence.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
    
    
    # DOF Rutime plot
    fig,ax = plt.subplots(figsize=(11.5, 12.5))
    ax.loglog(CADETFVdata['DOF'],CADETFVdata['runtime'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
        

        
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
    ax.set_xlabel('Degrees of freedom', fontsize=25)
    ax.set_ylabel('Simulation time (s)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.45)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_runtime.svg'),format = 'svg',dpi = 1200)
    
    
    # Runtime Error plot
    fig,ax = plt.subplots(figsize=(11.5, 10))
    ax.loglog(CADETFVdata['runtime'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.loglog(CADETJuliadata["runtime_e"],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata["runtime_i"],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax.loglog(CADETJuliadata['runtime_e'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['runtime_i'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])

        
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        ax.loglog(CADETDGdata['runtime_e'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        ax.loglog(CADETDGdata['runtime_i'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
   
    ax.set_xlabel('Simulation time (s)', fontsize=25)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.4)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_err_runtime.svg'),format = 'svg',dpi = 1200)
    
    
    #Plotting the profiles
    fig,ax = plt.subplots(figsize=(7, 4)) #figsize=(11.5, 10)
    if 'SMA' in saveLocation: #if having the SMA isotherm
    
        #Counting number of components as number of x-1
        x_columns = len(set([col for col in profileData.columns if col.startswith('x')]))
        for i in range(x_columns - 1):
            idxx = "x{}".format(i + 2)
            ax.plot( profileData["time"],profileData[idxx], '--', label = "$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell1"][0]),color = colors_profile1[i])
            idxx = "y{}".format(i + 2)
            ax.plot(profileData["time"],profileData[idxx], label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell2"][0]),color = colors_profile2[i])
    else: #If not having the SMA isotherm
        #Counting number of components as number of x-1
        x_columns = len(set([col for col in profileData.columns if col.startswith('x')]))
        for i in range(x_columns):
            idxx = "x{}".format(i + 1)
            ax.plot( profileData["time"],profileData[idxx], '--',label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell1"][0]),color = colors_profile1[i])
            idxx = "y{}".format(i + 1)
            ax.plot(profileData["time"],profileData[idxx], label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell2"][0]),color = colors_profile2[i])

    ax.set_xlabel('Time (s)', fontsize=15)
    ax.set_ylabel('Concentration (mol/m$^3$)', fontsize=15)
    ax.legend(fontsize=10)
    plt.savefig(os.path.join(saveLocation,'plot_profiles.svg'),format = 'svg',dpi = 1200)
    
    
    #Subplots with profiles, simulation time vs. MAE, DOF vs. simulation time
    #Plotting the profiles
    fig,ax = plt.subplots(1,3,figsize=(14*2, 10)) #figsize=(11.5, 10)
    #Counting number of components as number of x-1
    if 'SMA' in saveLocation: #if having the SMA isotherm
    
        #Counting number of components as number of x-1
        x_columns = len(set([col for col in profileData.columns if col.startswith('x')]))
        for i in range(x_columns - 1):
            idxx = "x{}".format(i + 2)
            ax[0].plot( profileData["time"],profileData[idxx],'--', label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell1"][0]),color = colors_profile1[i])
            idxx = "y{}".format(i + 2)
            ax[0].plot(profileData["time"],profileData[idxx], label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell2"][0]),color = colors_profile2[i])
    else: #If not having the SMA isotherm
        #Counting number of components as number of x-1
        x_columns = len(set([col for col in profileData.columns if col.startswith('x')]))
        for i in range(x_columns):
            idxx = "x{}".format(i + 1)
            ax[0].plot( profileData["time"],profileData[idxx], '--', label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell1"][0]),color = colors_profile1[i])
            idxx = "y{}".format(i + 1)
            ax[0].plot(profileData["time"],profileData[idxx], label="$c_{}$, $N_e^b$ = {}".format(i + 1, profileData["nCell2"][0]),color = colors_profile2[i])

    ax[0].set_xlabel('Time (s)', fontsize=25)
    ax[0].set_ylabel('Concentration (mol/m$^3$)', fontsize=25)
    ax[0].legend(fontsize=20)
    
    #Plotting simulation time vs MAE
    ax[1].loglog(CADETFVdata['runtime'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.loglog(CADETJuliadata["runtime_e"],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata["runtime_i"],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax[1].loglog(CADETJuliadata['runtime_e'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax[1].loglog(CADETJuliadata['runtime_i'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
        
        
    # Plot CADET-DG if available
    if len(CADETDGdata) != 0:
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax[1].loglog(CADETDGdata['runtime_e'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
            ax[1].loglog(CADETDGdata['runtime_i'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
    # if len(CADETDGdata) != 0:
    #     for i in range(CADETDGdata[tag].nunique()):
    #         idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
    #         ax.loglog(CADETDGdata['runtime_e_ode'][idx],CADETDGdata["maxE_e_ode"][idx],'.--', label = f'CADET-DG, Exact-ode, {plottag}={CADETDGdata[tag][idx].min()}' )
            # ax.loglog(CADETDGdata['runtime_i_ode'][idx],CADETDGdata["maxE_i_ode"][idx],'.--', label = f'CADET-DG, Collocation-ide, {plottag}={CADETDGdata[tag][idx].min()}' )
    
    ax[1].set_xlabel('Simulation time (s)', fontsize=25)
    ax[1].legend(fontsize=12)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax[1].set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax[1].grid(True, which='both', linestyle='--', linewidth=0.5)
    ax[1].tick_params(axis='both', which='major', labelsize=22)
    
    
    #Plotting simulation time vs DOF
    ax[2].loglog(CADETFVdata['DOF'],CADETFVdata['runtime'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax[2].loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax[2].loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
        
        
    # Plot CADET-DG if available
    if len(CADETDGdata) != 0:
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax[2].loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
            ax[2].loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
    
    ax[2].set_xlabel('Degrees of freedom', fontsize=25)
    ax[2].set_ylabel('Simulation time (s)', fontsize=25)
    ax[2].grid(True, which='both', linestyle='--', linewidth=0.5)
    ax[2].tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax[2].legend(fontsize=12)
    plt.savefig(os.path.join(saveLocation,'plot_subplot.svg'),format = 'svg',dpi = 1200)
    
    

    ################ sundials ida dae comparison ################
    # For the sundials ida dae comparison 
    # the IDA solver used for solving the DAE equations where
    # jacobians were determined using finite difference or automatic differentiation 
    # for which the difference should be very small. 
    if 'runtime_dae_e'in CADETJuliadata.columns and 'runtime_e_dae'in CADETDGdata.columns:
        
        # DOF error plot 
        fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
        
        # To match the same number of polynomial degrees for the dae comparison
        polydae = 0
        
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            if CADETJuliadata['runtime_dae_e'][idx].iloc[0] == 0:
                continue
            else:
                ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_dae_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
                ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_dae_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i] )
                polydae += 1
                
        
        # Plot CADET-DG 
        for i in range(polydae):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            if CADETDGdata['runtime_e_ode'][idx].iloc[0] == 0:
                continue
            else:
                ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_e_dae"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
                ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_i_dae"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
    
    
        ax.set_xlabel('Degrees of freedom', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend()
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_convergence_dae.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
        
        
        # DOF runtime plot 
        fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
        
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            if CADETJuliadata['runtime_dae_e'][idx].iloc[0] == 0:
                continue
            else:
                ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_dae_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
                ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_dae_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i] )
                
        
        # Plot CADET-DG if available
        for i in range(polydae):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            if CADETDGdata['runtime_e_ode'][idx].iloc[0] == 0:
                continue
            else:
                ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_e_dae"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
                ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i_dae"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
    
    
        ax.set_xlabel('Degrees of freedom', fontsize=25)
        ax.set_ylabel('Simulation time (s)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_runtime_dae.svg'),format = 'svg',dpi = 1200)
        
        
        # runtime error plot 
        fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
        
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            if CADETJuliadata['runtime_dae_e'][idx].iloc[0] == 0:
                continue
            else:
                ax.loglog(CADETJuliadata['runtime_dae_e'][idx],CADETJuliadata["maxE_dae_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
                ax.loglog(CADETJuliadata['runtime_dae_i'][idx],CADETJuliadata["maxE_dae_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i] )
                
        
        # Plot CADET-DG if available
        for i in range(polydae):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            if CADETDGdata['runtime_e_ode'][idx].iloc[0] == 0:
                continue
            else:
                ax.loglog(CADETDGdata['runtime_e_dae'][idx],CADETDGdata["maxE_e_dae"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
                ax.loglog(CADETDGdata['runtime_i_dae'][idx],CADETDGdata["maxE_i_dae"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
    
    
        ax.set_xlabel('Simulation time (s)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_err_runtime_dae.svg'),format = 'svg',dpi = 1200)
        
    
    
    ################ kinetic comparison for approximating rapid eq ################
    if 'runtime_e_ode'in CADETDGdata.columns:
        
        fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
        ax.loglog(CADETFVdata['DOF'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
        
        # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
        # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
            ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2 ,color=colorDGJulia_inexact[i])
            
        
        # Plot CADET-DG 
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_e_ode"][idx],'-', label = f'CADET-DG kin, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
            ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_i_ode"][idx],'-', label = f'CADET-DG kin, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])


        ax.set_xlabel('Degrees of freedom', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend()
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_convergence_kin.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
        
        
        # DOF Rutime plot
        fig,ax = plt.subplots(figsize=(11.5, 10))
        ax.loglog(CADETFVdata['DOF'],CADETFVdata['runtime'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
        # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_e"],'.--', label = 'CADET-Julia, Exact')
        # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_i"],'.--', label = 'CADET-Julia, Collocation')
        
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
            ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])

            
        # Plot CADET-DG 
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_e"][idx],'-', label = f'CADET-DG kin, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
            ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i"][idx],'-', label = f'CADET-DG kin, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
                
        ax.set_xlabel('Degrees of freedom', fontsize=25)
        ax.set_ylabel('Simulation time (s)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_runtime_kin.svg'),format = 'svg',dpi = 1200)
        
        
        # Runtime Error plot
        fig,ax = plt.subplots(figsize=(11.5, 10))
        ax.loglog(CADETFVdata['runtime'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
        # plt.loglog(CADETJuliadata["runtime_e"],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
        # plt.loglog(CADETJuliadata["runtime_i"],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
        
        for i in range(CADETJuliadata[tag].nunique()):
            idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
            ax.loglog(CADETJuliadata['runtime_e'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
            ax.loglog(CADETJuliadata['runtime_i'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])

            
        # Plot CADET-DG 
        for i in range(CADETDGdata[tag].nunique()):
            idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
            ax.loglog(CADETDGdata['runtime_e'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG kin, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
            ax.loglog(CADETDGdata['runtime_i'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG kin, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
                
       
        ax.set_xlabel('Simulation time (s)', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'Plot_err_runtime_kin.svg'),format = 'svg',dpi = 1200)
    
    
    
    ############ Plotting only Collocation ############
    fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
    ax.loglog(CADETFVdata['DOF'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    
    # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        # ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i] )
        # ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_fbdf"][idx],'.--', label = f'CADET-Julia, FBDF, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_exact[i] )

    
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        # ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])


    ax.set_xlabel('Degrees of freedom', fontsize=25)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend()
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_convergence_i.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
    
    
    # DOF Rutime plot
    fig,ax = plt.subplots(figsize=(11.5, 10)) #
    ax.loglog(CADETFVdata['DOF'],CADETFVdata['runtime'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        # ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_i"][idx],'.--', label = f'CADET-Julia, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
        # ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_fbdf"][idx],'.--', label = f'CADET-Julia, FBDF, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        

        
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        # ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i"][idx],'-', label = f'CADET-DG, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
    ax.set_xlabel('Degrees of freedom', fontsize=25)
    ax.set_ylabel('Simulation time (s)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_runtime_i.svg'),format = 'svg',dpi = 1200)
    
    
    # Runtime Error plot
    fig,ax = plt.subplots(figsize=(11.5, 11)) #
    ax.loglog(CADETFVdata['runtime'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.loglog(CADETJuliadata["runtime_e"],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata["runtime_i"],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        # ax.loglog(CADETJuliadata['runtime_e'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['runtime_i'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
        # ax.loglog(CADETJuliadata['runtime_fbdf'][idx],CADETJuliadata["maxE_fbdf"][idx],'.--', label = f'CADET-Julia, FBDF, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])

        
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        # ax.loglog(CADETDGdata['runtime_e'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        ax.loglog(CADETDGdata['runtime_i'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
   
    ax.set_xlabel('Simulation time (s)', fontsize=25)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_err_runtime_i.svg'),format = 'svg',dpi = 1200)
    
    
    
    
    ############ Plotting only Julia exact vs. collocation ############
    fig,ax = plt.subplots(figsize=(11.5, 10)) #figsize=(15, 13)
    # ax.loglog(CADETFVdata['DOF'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    
    # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata['DOF'],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}',markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i] )

    
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        # ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        # ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])


    ax.set_xlabel('Degrees of freedom', fontsize=25)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend()
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_convergence_julia.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
    
    
    # DOF Rutime plot
    fig,ax = plt.subplots(figsize=(11.5, 10))
    # ax.loglog(CADETFVdata['DOF'],CADETFVdata['runtime'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.plot(CADETJuliadata['DOF'],CADETJuliadata["runtime_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['DOF'][idx],CADETJuliadata["runtime_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])
        
        
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        # ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        # ax.loglog(CADETDGdata['DOF'][idx],CADETDGdata["runtime_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
    ax.set_xlabel('Degrees of freedom', fontsize=25)
    ax.set_ylabel('Simulation time (s)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_runtime_julia.svg'),format = 'svg',dpi = 1200)
    
    
    # Runtime Error plot
    fig,ax = plt.subplots(figsize=(11.5, 11))
    # ax.loglog(CADETFVdata['runtime'],CADETFVdata['maxE'],':', label = 'CADET-FV',markersize=markersize, marker = '^', linewidth=2, color = colorFV)
    # plt.loglog(CADETJuliadata["runtime_e"],CADETJuliadata["maxError_e"],'.--', label = 'CADET-Julia, Exact')
    # plt.loglog(CADETJuliadata["runtime_i"],CADETJuliadata["maxError_i"],'.--', label = 'CADET-Julia, Collocation')
    
    for i in range(CADETJuliadata[tag].nunique()):
        idx = slice(i * CADETJuliadata["nCellu"].nunique(), (i + 1) * CADETJuliadata["nCellu"].nunique())
        ax.loglog(CADETJuliadata['runtime_e'][idx],CADETJuliadata["maxE_e"][idx],'.--', label = f'CADET-Julia, Exact, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_exact[i])
        ax.loglog(CADETJuliadata['runtime_i'][idx],CADETJuliadata["maxE_i"][idx],'.--', label = f'CADET-Julia, Collocation, {plottag}={CADETJuliadata[tag][idx].min()}' ,markersize=markersize, linewidth=2,color=colorDGJulia_inexact[i])

        
    # Plot CADET-DG 
    for i in range(CADETDGdata[tag].nunique()):
        idx = slice(i * CADETDGdata["nCellu"].nunique(), (i + 1) * CADETDGdata["nCellu"].nunique())
        # ax.loglog(CADETDGdata['runtime_e'][idx],CADETDGdata["maxE_e"][idx],'-', label = f'CADET-DG, Exact, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_exact[i])
        # ax.loglog(CADETDGdata['runtime_i'][idx],CADETDGdata["maxE_i"][idx],'-', label = f'CADET-DG, Collocation, {plottag}={CADETDGdata[tag][idx].min()}' ,markersize=markersize, marker = '*', linewidth=2,color=colorDG_inexact[i])
            
   
    ax.set_xlabel('Simulation time (s)', fontsize=25)
    # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=22)
    # plt.title('LRM Langmuir')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
    fig.subplots_adjust(bottom=0.38)  # Adjust this value as needed
    plt.savefig(os.path.join(saveLocation,'Plot_err_runtime_julia.svg'),format = 'svg',dpi = 1200)
    
    
    # Plotting GSM and DGSEM for CADET-DG 
    if os.path.exists(path + "GSM/CADETDGConvergence.csv"):
        GSMData = pd.read_csv(path + "GSM/CADETDGConvergence.csv")
        # For this data, '_e' marks that GSM is used, _i marks DGSEM is used. 
        # Only collocation is tested here. 
        ncelpar = 'nCellsParu'
        lines = ['--', '-', ':',':']
        markers = ['.','*', '^','h']
        colors1 = ['tab:blue', 'tab:green', 'tab:purple', 'tab:pink', ] #'olive'
        colors2 = ['tab:orange', 'tab:red', 'tab:brown', 'tab:gray', ] #'cyan'
        
        ## First GSM vs DGSEM is compared for a single element in the particle phase 
        # THen DGSEM at various particle elements are compared. 
        # This is plotted in one plot. 
        
        # Convergence plot
        fig,ax = plt.subplots(figsize=(9, 9))
        for i in range(GSMData['nCellsParu'].nunique()):
            start = GSMData[GSMData['nCellsParu'] == i+1].index[0]
            stop = GSMData[GSMData['nCellsParu'] == i+1].index[-1]+1
            idx = slice(start,stop)
            ax.loglog(GSMData['DOF'][idx],GSMData["maxE_i"][idx],lines[i], label = f'DGSEM, $N_e^p$={GSMData[ncelpar][idx].min()}' ,markersize=markersize, marker = markers[i], linewidth=2, color = colors1[i % len(colors2)])
            
        idx = slice(0, GSMData["polyDegPoreu"].nunique())
        ax.loglog(GSMData['DOF'][idx],GSMData["maxE_e"][idx],lines[-1], label = 'GSM' ,markersize=markersize, marker = markers[-1], linewidth=2, color = colors2[0])

        ax.set_xlabel('Degrees of freedom', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend()
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.25)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'GSM/Plot_convergence_GSM.svg'),format = 'svg',dpi = 1200, bbox_inches='tight')
        
        
        # DOF Runtime 
        fig,ax = plt.subplots(figsize=(9, 9))
        for i in range(GSMData['nCellsParu'].nunique()):
            start = GSMData[GSMData['nCellsParu'] == i+1].index[0]
            stop = GSMData[GSMData['nCellsParu'] == i+1].index[-1]+1
            idx = slice(start,stop)
            ax.loglog(GSMData['DOF'][idx],GSMData["runtime_i"][idx],lines[i], label = f'DGSEM, $N_e^p$={GSMData[ncelpar][idx].min()}' ,markersize=markersize, marker = markers[i], linewidth=2, color = colors1[i % len(colors2)])
        
        idx = slice(0, GSMData["polyDegPoreu"].nunique())
        ax.loglog(GSMData['DOF'][idx],GSMData["runtime_e"][idx],lines[-1], label = 'GSM' ,markersize=markersize, marker = markers[-1], linewidth=2, color = colors2[0])
    
                
        ax.set_xlabel('Degrees of freedom', fontsize=25)
        ax.set_ylabel('Simulation time (s)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.25)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'GSM/Plot_runtime.svg'),format = 'svg',dpi = 1200)
            
        
        # Plot Runtime error 
        fig,ax = plt.subplots(figsize=(11, 9))
        for i in range(GSMData['nCellsParu'].nunique()):
            start = GSMData[GSMData['nCellsParu'] == i+1].index[0]
            stop = GSMData[GSMData['nCellsParu'] == i+1].index[-1]+1
            idx = slice(start,stop)
            ax.loglog(GSMData['runtime_i'][idx],GSMData["maxE_i"][idx],lines[i], label = f'DGSEM, $N_e^p$={GSMData[ncelpar][idx].min()}' ,markersize=markersize, marker = markers[i], linewidth=2, color = colors1[i % len(colors2)])
            
        idx = slice(0, GSMData["polyDegPoreu"].nunique())
        ax.loglog(GSMData['runtime_e'][idx],GSMData["maxE_e"][idx],lines[-1], label = 'GSM' ,markersize=markersize, marker = markers[-1], linewidth=2, color = colors2[0])
       
        ax.set_xlabel('Simulation time (s)', fontsize=25)
        # ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.set_ylabel('Max abs error (mol/m$^3$)', fontsize=25)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=22)
        # plt.title('LRM Langmuir')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
        ax.legend(fontsize=20, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, framealpha=1.0)
        fig.subplots_adjust(bottom=0.25)  # Adjust this value as needed
        plt.savefig(os.path.join(saveLocation,'GSM/Plot_err_runtime.svg'),format = 'svg',dpi = 1200)
    
    
    
    


# A function to find data and initiate the plot function 
def plot_initiator(path,no_bind = False):
    if no_bind == True:
        CADETJuliadata = pd.read_csv(path + 'CADETJuliaConvergence.csv')
        CADETDGdata = pd.read_csv(path + 'CADETDGConvergence.csv')
        
        # Plots
        if path[-4] == "G": # If using the GRM
     
            plot_convergence(pd.DataFrame(),CADETJuliadata[:],CADETDGdata[:],pd.DataFrame(),path, "GRM")
        else:
            plot_convergence(pd.DataFrame(),CADETJuliadata[:],CADETDGdata[:],pd.DataFrame(),path)
            
        return
        

    CADETFVdata = pd.read_csv(path + 'CADETFVConvergence.csv')
    CADETJuliadata = pd.read_csv(path + 'CADETJuliaConvergence.csv')
    CADETDGdata = pd.read_csv(path + 'CADETDGConvergence.csv')
    profileData = pd.read_csv(path + 'Profiles_data.csv', delimiter=",")

    
    # Compare the speed up and convergence between CADET-DG and CADET-Julia
    comparison = pd.DataFrame({'SpeedUp' : CADETDGdata['runtime_i'] / CADETJuliadata['runtime_i'], 
                              'AvgSpeedUp' : np.mean(CADETDGdata['runtime_i'] / CADETJuliadata['runtime_i'])*np.ones(len(CADETDGdata['runtime_i'])),
                              'DiffMae' : CADETDGdata['maxE_i'] - CADETJuliadata['maxE_i']})  
    comparison.to_csv(path + 'comparison.csv')


    comparison_speed = pd.read_csv('comparison_speedup.csv',index_col=0)
    # if LRMP
    if path[-2] == "P": 
        row = 'LRMP'
        
    # if LRM
    elif path[-4] == "L": 
        row = 'LRM'
    
    # if GRM
    else: 
        row = 'GRM'
        
    # if linear isotherm
    if path[1] == "i":  
        col = 'Linear'
        
    # if langmuir isotherm 
    elif path[1] == "a": 
        col = 'Langmuir'
    
    # if SMA isotherm
    else :
        col = 'SMA'
        
    comparison_speed.loc[row,col] = comparison['AvgSpeedUp'][0]
    comparison_speed.to_csv('comparison_speedup.csv')
    
    # Plots
    if path[-4] == "G": # If using the GRM
 
        plot_convergence(CADETFVdata,CADETJuliadata[:],CADETDGdata[:],profileData,path, "GRM")
    else:
        plot_convergence(CADETFVdata,CADETJuliadata[:],CADETDGdata[:],profileData,path)


    
    
#%%
# Run the convergence function to plot the Benchmarks 
path = "Linear/Batch/LRM/"
plot_initiator(path)

path = "Linear/Batch/LRMP/"
plot_initiator(path)

path = "Linear/Batch/GRM/"
plot_initiator(path)


path = "Langmuir/Batch/LRM/"
plot_initiator(path)

path = "Langmuir/Batch/LRMP/"
plot_initiator(path)

path = "Langmuir/Batch/GRM/"
plot_initiator(path)


path = "SMA/Batch/LRM/"
plot_initiator(path)

path = "SMA/Batch/LRMP/"
plot_initiator(path)

path = "SMA/Batch/GRM/"
plot_initiator(path)


path = "No_binding/Batch/LRM/"
plot_initiator(path, True)

path = "No_binding/Batch/LRMP/"
plot_initiator(path, True)

path = "No_binding/Batch/GRM/"
plot_initiator(path, True)
