import numpy as np


def get_error(fname):
    """get train and test error from log file"""
    
    with open(fname, "r") as log_file:
        train_flag = False
        for line in log_file:
            if train_flag:
                train_error = float(line.strip())
                train_flag = False
            if "Total error" in line:
                train_flag = True
            if "Test error" in line:
                test_error = float(line.replace("Test error:", "").strip())
    return train_error, test_error


def isImprovedByReplacement(individual):
    if individual.info:
        pfit = individual.info.get("pfit")
        ifit = individual.error_vector
        return np.count_nonzero(pfit) > np.count_nonzero(ifit)
    return False