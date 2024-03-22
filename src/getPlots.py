import matplotlib.pyplot as plt
import numpy as np
def plot_params(names, curve,final_fit ,output_dir):
    """
    Saves the DNA/Lp, DNA/Lc, DNA/St for each sample in a plot.
    Only uses the extension curves.

    Args:
    sample_name (list): List of sample names
    final_fit (dict): Dictionary of fits
    output_dir (str): Directory to save the plot

    Returns:
    None


    """
    extension_name = names
    extension = []
    extension_error = []
 
    for i in names:
        if curve == "both" and "extension" in i:
            # extension_name.append(i)
            extension.append([final_fit[i]['DNA/Lp'].value,final_fit[i]['DNA/Lc'].value,final_fit[i]['DNA/St'].value])
            extension_error.append([final_fit[i]['DNA/Lp'].stderr,final_fit[i]['DNA/Lc'].stderr,final_fit[i]['DNA/St'].stderr]  )
        elif curve == "extension" or curve == "retraction":
            extension.append([final_fit[i]['DNA/Lp'].value,final_fit[i]['DNA/Lc'].value,final_fit[i]['DNA/St'].value])
            extension_error.append([final_fit[i]['DNA/Lp'].stderr,final_fit[i]['DNA/Lc'].stderr,final_fit[i]['DNA/St'].stderr]  )

    plt.figure()
    # DNA/Lp plot
    plt.subplot(1, 3, 1)
    plt.errorbar(extension_name,np.array(extension)[:,0],yerr=np.array(extension_error)[:,0],fmt='o-',label="Extension", color='blue')
    plt.xticks(rotation=45)
    plt.title('DNA/Lp(nm)')
  

    # DNA/Lc plot
    plt.subplot(1, 3, 2)
    plt.errorbar(extension_name,np.array(extension)[:,1],yerr=np.array(extension_error)[:,1],fmt='o-',label="Extension", color='blue')
    plt.xticks(rotation=45)
    plt.title('DNA/Lc(micron)')


    # DNA/St plot
    plt.subplot(1, 3, 3)
    plt.errorbar(extension_name,np.array(extension)[:,2],yerr=np.array(extension_error)[:,2],fmt='o-',label="Extension", color='blue')
    plt.title('DNA/St(pN)')
    plt.xticks(rotation=45)
    plt.tight_layout()


    plt.savefig(output_dir+'/DNA_Lp_Lc_St.png')


def plot_fits(sample_name, final_fit, output_dir,useLog):
    """
    Saves the fits for each sample in a plot.
    Note: The y-axis is in log scale.
    
    Args:
    sample_name (list): List of sample names
    final_fit (dict): Dictionary of fits
    output_dir (str): Directory to save the plot

    Returns:
    None
    
    """



    fig, ax = plt.subplots()
   
    for i in sample_name:
        final_fit[i].plot()
    # put legend outside the plot
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=len(sample_name))
    plt.ylabel('Force (pN)',fontsize=16)

    plt.title('Force vs Distance',fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Distance (nm)',fontsize=16)

    plt.grid(True)
    if useLog:
        plt.ylabel('Log Force (pN)',fontsize=16)
        plt.yscale('log')
    plt.tight_layout()
    plt.savefig(output_dir+'/fit.png',bbox_inches='tight')


def plot_rawdata(force_distance_dict, output_dir,useLog):
    """
    Saves the raw data for each sample in a plot.
    Note: The y-axis is in log scale.
    Args:
    force_distance_dict (dict): Dictionary of force distance arrays
    output_dir (str): Directory to save the plot

    Returns:
    None
    """
    fig, ax = plt.subplots()
    # small size

    for key, value in force_distance_dict.items():
        ax.plot(value[1], value[0], label=key)
      
   
    # put legend outside the plot
    plt.xlabel('Distance (nm)')
    plt.ylabel('Force (pN)')
    plt.title('Force vs Distance',fontsize=16)  
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if useLog == True:
        plt.ylabel('Log Force (pN)')
        plt.yscale('log')
    plt.tight_layout()
    plt.savefig(output_dir+'/rawdata.png')
    
