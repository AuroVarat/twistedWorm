# TWLC Fitting for Optical Tweezer Data

## Table of Contents

- [TWLC Fitting for Optical Tweezer Data](#twlc-fitting-for-optical-tweezer-data)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Model](#model)
  - [Advanced Usage](#advanced-usage)
    - [1. Filtering Data](#1-filtering-data)
    - [2. Custom Initial Guesses](#2-custom-initial-guesses)
    - [3. Custom Model](#3-custom-model)

## Installation

If you do not have the conda environment, you can create a new environment using the following command.

`conda create -n pylake conda=23.7.2`



Then you can activate the environment using the following command.
`conda activate pylake`

Add conda-forge to the list of channels you can install packages from using the following command.
`conda config --add channels conda-forge`

Then you can install the required packages using the following command.
`conda install --file requirements.txt`
This will create a new environment with the name env and install all the required packages.

Make sure to have the conda env python in the PATH. You can check this by running the following command.
`which python`

If it is not in the PATH, you can add it to the PATH using the following command.
`export PATH=$PATH:/home/user/anaconda3/envs/pylake/bin:$PATH`


## Basic Usage

Add all the .h5 files in the data folder under a subfolder with a name ( say 'my-data' ). Then you have to set up the folder inside the input.txt, where you have to specify the folder name. You can also specify output folder name.

**input.txt**
```
#PARAM VALUE
Source data/<my-data>
Export data/<my-output>
Filter true 
Curve both
```

Make sure you are in the directory with main.py. Then run the following command.
`python main.py`

## Model

The twistable worm-like chain (tWLC) model, which better describes the untwisting behavior of DNA observed in the 30-60 pN force range. However, applying this model introduces challenges due to its complexity.

Parameter estimation poses a significant challenge, often relying on initial guesses. If these initial guesses are poor, the optimization process may converge to suboptimal parameter sets, known as local optima. To mitigate this issue, it's crucial to start with better initial values.

In our approach, we first fit the data within the range before the force begins to plateau (i.e., below 30 pN) using a standard worm-like chain model. We then utilize the estimated parameters from this fit as initial guesses for fitting the tWLC model.

Furthermore, experimental data might contain small offsets. These offsets could arise from variations in bead diameter between experiments or slight force drifts. To account for such offsets, we incorporate offset parameters for both distance and force, thereby compensating for any small discrepancies present in the data.

## Advanced Usage

### 1. Filtering Data
**input.txt**
```html
#PARAM VALUE
Source data/<my-data>
Export data/<my-output>
Filter true 
Curve both
useLog true
```

You can set Filter to false. This will not filter the data if it contains any negative values for distance.
And for the Curve, you can set it to 'both', 'extension' or retraction 'force'. This will then analyse the data for both the curves or only for the extension or retraction curve.
useLog is set to true, then the log of the y-axis will be taken. This is useful when the data is not linear.

### 2. Custom Initial Guesses
**default.txt**
```html
#PARAMS VALUE TYPE DESCRIPTION
DNA/d_offset 0.01 upper_bound distance-d_offset
DNA/d_offset    -0.01 lower_bound distance_d_offset
DNA/C       440 value   twist-rigidity
DNA/C   true    fixed   twist-rigidity
DNA/Fc  30.6    value   critical-force
DNA/Fc  true    fixed   critical-force
```
You can set the initial guesses for the parameters in the default.txt file. You can also set the upper and lower bounds for the parameters. You can also fix the parameters by setting the fixed to true. You can also add new parameters to the default.txt file that are compatible with PyLake.


### 3. Custom Model
**model.py**
```python
def initial_guess_model():
    """
    This function returns a model that can be used to estimate the initial guess for the fitting procedure.
    Default is the Odijk model.
    
    """
    return lk.ewlc_odijk_force("DNA").subtract_independent_offset() + lk.force_offset("DNA")

def final_fit_model():
    """
    This function returns a model that can be used to fit the final model.
    Default is the tWLC model.
    
    """

    return lk.twlc_force("DNA").subtract_independent_offset() + lk.force_offset("DNA")
```

You can also set the custom model for the initial guess and the final fit. You can also add new parameters to the model that are compatible with PyLake.
