import numpy as np



def getParams(input_dir, output_dir, sample_name, final_fit):
    """
    Saves the fit parameters for each sample in a text file.

    Args:
    input_dir (str): Directory to save the input
    output_dir (str): Directory to save the output
    sample_name (list): List of sample names
    final_fit (dict): Dictionary of fits

    Returns:
    None
    """
    values = []
    for i in sample_name:
        values.append([i]+[final_fit[i].params[j].value for j in final_fit[i].params.keys()])
    np.savetxt(output_dir+'/values.txt',values,fmt='%s',header='Sample Name,'+','.join(list(final_fit[sample_name[0]].params.keys())),delimiter=',')

def getForceDistance(input_dir, output_dir, force_distance_dict):
    """
    Save the force distance arrays to a file of sample name 

    Args:
    input_dir (str): Directory to save the input
    output_dir (str): Directory to save the output
    force_distance_dict (dict): Dictionary of force distance arrays

    Returns:
    None
    """
    sample_name = list(force_distance_dict.keys())
    for i, (force_array,distance_array) in enumerate(force_distance_dict.values()):
        np.savetxt(output_dir+'/'+sample_name[i]+'.txt',np.array([force_array,distance_array]).T,fmt='%s',header='Force,Distance',delimiter=',')
