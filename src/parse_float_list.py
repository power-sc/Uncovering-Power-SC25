import numpy as np

def parse_float_list(x):
    try:
        return list(map(float, x.split(',')))
    except:
        return np.nan