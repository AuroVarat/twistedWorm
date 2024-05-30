# TWLC Fitting for Optical Tweezer Data
<!-- add contributor -->
Auro Varat Patnaik

The program is strongly based on : [Lumicks Example](https://lumicks-pylake.readthedocs.io/en/stable/examples/twlc_fitting/twlc_fitting.html)
<!-- add license -->
## Table of Contents

- [TWLC Fitting for Optical Tweezer Data](#twlc-fitting-for-optical-tweezer-data)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Model](#model)
  - [Advanced Usage](#advanced-usage)
    - [1. Filtering Data](#1-filtering-data)
    - [2. Custom Model](#2-custom-model)
    - [3. Custom Initial Guesses](#3-custom-initial-guesses)

## Installation

The conda environment file is provided in the repository. You can create the environment using the following command.

`conda env create -f twistedWorm.yml`

Then activate the environment using the following command.

`conda activate tworm`


The repository has been provded with a set of sample data under `data/sample_data`. If you now run,

`python main.py`

It will fit the data in the `data/sample_data` folder and export the results in the `data/output` folder.


## Basic Usage

If you want to analyse your own datafiles, add all your .h5 files in the 'data' folder under a subfolder with a name ( say 'my-data' ).

Then in `src/input.txt` you have to set up a few things, you have to specify the folder name for your input data. You have to also specify a output folder name, it will be created in the data folder.

**src/input.txt**
```
#PARAM VALUE
Source data/<my-data>
Export data/<my-output>
Filter true 
Curve both
useLog true
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
Filter 1
Curve both
useLog 1
```

You can set Filter to false (set to 0). This will not filter the data if it contains any negative values for distance.
And for the Curve, you can set it to 'both', 'extension' or 'retraction'. This will then analyse the data for both the curves or only for the extension or retraction curve.
useLog is set to true, then the log of the y-axis will be taken. This is useful when the data is not linear.

To change true to false, change 1 to 0.


### 2. Custom Model

There are two default models provided in the model.py file. The initial_guess_model and the final_fit_model. The initial_guess_model is used to estimate the initial guess for the final fitting procedure, by default this uses the standard worm-like chain model. 

Then with better guesses from initial_guess_model, the final_fit_model is used to fit the final model. By default, this uses the tWLC model.

You can change either of the model to your custom model. But this needs to be compatible with PyLake (recommend looking into their documentation).


 :warning: **If you are using custom model**: If you modify the initial_guess_model, make sure to modify the initial_guess_params.txt file to match the parameters of the model. If you modify the final_fit_model, make sure to modify the default.txt file to match the parameters of the model. This is described in the next section.



**src/model.py**
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




### 3. Custom Initial Guesses

For the fitting params, you have two files - initial_guess_params.txt and default.txt. 

The initial_guess_params.txt sets the initial guesses for the initial standard worm-like chain model.If you wish to change the initial guesses, you can change the initial_guess_params.txt file. 

 The default.txt sets the initial guesses for the final tWLC model. If you wish to change the initial guesses, you can change the default.txt file.

 Note: default.txt should consists of parameters that are part of your final model but not in the initial_guess_params.txt file. Because the final model inherits the parameters from the initial_guess_params.txt file.

**default.txt**
```html
#PARAMS VALUE TYPE DESCRIPTION
DNA/C       440 value   twist-rigidity
DNA/C   true    fixed   twist-rigidity
DNA/Fc  30.6    value   critical-force
DNA/Fc  true    fixed   critical-force
```
You can set the initial guesses for the parameters in the default.txt file. You can also set the upper and lower bounds for the parameters. You can also fix the parameters by setting the fixed to true. You can also add new parameters to the default.txt file that are compatible with PyLake.

This needs to be done for the final fit model.




