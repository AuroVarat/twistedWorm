"""
Created on March 8, 2024
Author: Auro Varat Patnaik
Email: auro.patnaik@ed.ac.uk
"""
# Importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
import lumicks.pylake as lk
import glob
import os

"""
Read the input.txt file to get the input and output directory.
The input directory should contain the .h5 files of the force distance curves
The output directory will contain the output files
The extraFilter is a boolean value to filter out negative values of distance
The whichCurve is a string to select the type of curve to be fitted. It can be "extension", "retraction" or "both"
"""

dir = np.genfromtxt("input.txt",dtype='str')
default = np.genfromtxt("default.txt",dtype='str')

input_dir = dir[0,1]    # input directory
output_dir = dir[1,1]  # output directory
extraFilter = dir[2,1] # extra filter to filter out negative values of distance
whichCurve = dir[3,1]   # which curve to fit
os.makedirs(output_dir, exist_ok=True) # create the output directory if it does not exist


"""
Read the force distance curves from the input directory and store them in a dictionary
"""
fdcurves = {}
keys = []
for filename in glob.glob(input_dir+'/*.h5'):
    file = lk.File(filename)
    for key, curve in file.fdcurves.items():
        fdcurves[key] = curve
        keys.append(key)



force_distance_dict = {}
for i, curve in enumerate(fdcurves.values()):
    peak = np.argmax(curve.d.data)

    # warning if curve.d.data has negative values
    if np.min(curve.d.data) < 0:
        print("Warning: curve " + keys[i] + " has negative values of distance. Filtering the data to discount negative values. You cannot disable this.")

    # Filter the data
   
    filtered_indices = np.where((curve.d.data > 1e-6)) # filter out negative values


    # comment either of them to get only extension or retraction
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
fig, ax = plt.subplots()
# small size
fig.set_size_inches(8, 3)
for key, value in force_distance_dict.items():
    ax.plot(value[1], value[0], label=key)
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Force (N)')
    ax.legend()
    ax.set_title('Force vs Distance')
    ax.grid(True)
# put legend outside the plot
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()


m_odijk = lk.ewlc_odijk_force("DNA").subtract_independent_offset() + lk.force_offset("DNA")
m_dna = lk.twlc_force("DNA").subtract_independent_offset() + lk.force_offset("DNA")



def set_params(fit, limit=None):
    for i in default[slice(*limit)]:
        setattr(fit[i[0]], i[2], float(i[1]))
    return fit


# Multiple Independent Fits
def independent_fits(force_distance_dict,model,initial_guess_dict=False,param_limit=None):
    fits = {}
    
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
    
    
    return fits


f_guess = independent_fits(force_distance_dict,m_odijk,initial_guess_dict=False,param_limit=(0,2))
final_fit = independent_fits(force_distance_dict,m_odijk,initial_guess_dict=f_guess,param_limit=(2,))


# Save the values of all params for each curve
values = []
for i in sample_name:
    values.append([i]+[final_fit[i].params[j].value for j in final_fit[i].params.keys()])
np.savetxt(output_dir+'/values.txt',values,fmt='%s',header='Sample Name,'+','.join(list(final_fit[sample_name[0]].params.keys())),delimiter=',')

"""
Save the force distance arrays to a file of sample name 
"""
for i, (force_array,distance_array) in enumerate(force_distance_dict.values()):
    np.savetxt(output_dir+'/'+sample_name[i]+'.txt',np.array([force_array,distance_array]).T,fmt='%s',header='Force,Distance',delimiter=',')


