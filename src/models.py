import lumicks.pylake as lk

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
    # return lk.ewlc_odijk_force("DNA").subtract_independent_offset() + lk.force_offset("DNA")

    return lk.twlc_force("DNA").subtract_independent_offset() + lk.force_offset("DNA")