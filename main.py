"""
Created on March 8, 2024
Author: Auro Varat Patnaik
Email: auro.patnaik@ed.ac.uk
"""
# Importing the required libraries
import numpy as np
import lumicks.pylake as lk
import glob
import os
from src import getPlots
from src import getFiles
from src import models as m
from tqdm import tqdm

"""
Read the input.txt file to get the input and output directory.
The input directory should contain the .h5 files of the force distance curves
The output directory will contain the output files
The extraFilter is a boolean value to filter out negative values of distance
The whichCurve is a string to select the type of curve to be fitted. It can be "extension", "retraction" or "both"
"""

dir = np.genfromtxt("src/input.txt",dtype='str')
default = np.genfromtxt("src/default.txt",dtype='str')

input_dir = dir[0,1]    # input directory
output_dir = dir[1,1]  # output directory
extraFilter = bool(dir[2,1]) # extra filter to filter out negative values of distance
whichCurve = dir[3,1]   # which curve to fit
useLog = bool(dir[4,1]) # use log scale for the fits
os.makedirs(output_dir, exist_ok=True) # create the output directory if it does not exist


"""
Read the .h5 files from the input directory and store the force distance curves in a dictionary
"""
fdcurves = {}
keys = []
for filename in glob.glob(input_dir+'/*.h5'):
    file = lk.File(filename)
    for key, curve in file.fdcurves.items():
        fdcurves[key] = curve
        keys.append(key)


"""
Read the force distance curves and store the force and distance arrays in a dictionary
"""
force_distance_dict = {}
for i, curve in enumerate(fdcurves.values()):
    peak = np.argmax(curve.d.data)

    # warning if curve.d.data has negative values
    if np.min(curve.d.data) < 0:
        print("Warning: curve " + keys[i] + " has negative values of distance. Filtering the data to discount negative values. You cannot disable this.")

    # Filter the data
    filtered_indices = np.where((curve.d.data > 1e-6)) # filter out negative values

  
    if whichCurve == "extension":
        force_extension = curve.f.data[filtered_indices][:peak]
        distance_extension = curve.d.data[filtered_indices][:peak]
        force_distance_dict[keys[i]] = [force_extension, distance_extension]
    elif whichCurve == "retraction":
        force_retraction = curve.f.data[filtered_indices][peak:]
        distance_retraction = curve.d.data[filtered_indices][peak:]
        force_distance_dict[keys[i]] = [force_retraction, distance_retraction]
    else:
        force_extension = curve.f.data[filtered_indices][:peak]
        distance_extension = curve.d.data[filtered_indices][:peak]
        force_retraction = curve.f.data[filtered_indices][peak:]
        distance_retraction = curve.d.data[filtered_indices][peak:]
        force_distance_dict[keys[i]+"_extension"] = [force_extension, distance_extension]
        force_distance_dict[keys[i]+"_retraction"] = [force_retraction, distance_retraction]



sample_name = list(force_distance_dict.keys())



        # using force_distance_dict to plot the fd curves with small plots for each curve

"""
    Setup for the fits
"""
m_odijk = m.initial_guess_model()
m_dna = m.final_fit_model()



def set_params(fit, limit=None):
    for i in default[slice(*limit)]:
        setattr(fit[i[0]], i[2], float(i[1]))
    return fit


# Multiple Independent Fits
def independent_fits(force_distance_dict,model,initial_guess_dict=False,param_limit=None):
    fits = {}
    if not initial_guess_dict: 
        print("Finding initial guess by fitting Odijk model")
    else:
        print("Fitting TWLC model")
    with tqdm(total=len(force_distance_dict.keys())) as pbar:
        for i, (force_array,distance_array) in enumerate(force_distance_dict.values()):
            # Add a dataset to the fit
        
            fit = lk.FdFit(model)
        
            if initial_guess_dict == False:
                # This means we are fitting the Odijk model, so we filter data to get forces < 30
         
                mask = force_array < 30
                force_array = force_array[mask]
                distance_array = distance_array[mask]

            fit.add_data(sample_name[i], force_array, distance_array) 
                
            if initial_guess_dict:
                
                fit.update_params(initial_guess_dict[sample_name[i]])

            fit = set_params(fit,param_limit)
            fit.fit()

            fits[sample_name[i]] = fit
            pbar.update(1)
    
    
    return fits

"""
Initial Guess using the Odijk model
"""
f_guess = independent_fits(force_distance_dict,m_odijk,initial_guess_dict=False,param_limit=(0,2))

"""
Then use the parameters from the Odijk model to fit the DNA model
"""
final_fit = independent_fits(force_distance_dict,m_odijk,initial_guess_dict=f_guess,param_limit=(2,))


# Save the values of all params for each curve


getFiles.getForceDistance(input_dir, output_dir, force_distance_dict)# save the force distance arrays
getFiles.getParams(input_dir, output_dir, sample_name, final_fit)# save the fit parameters for each sample in a text file


getPlots.plot_params(sample_name,whichCurve,final_fit,output_dir) # plot the fit parameters for each sample in a plot

getPlots.plot_rawdata(force_distance_dict, output_dir,useLog) # save the raw data for each sample in a plot
getPlots.plot_fits(sample_name,final_fit,output_dir,useLog) # save the fits for each sample in a plotn along with the raw data