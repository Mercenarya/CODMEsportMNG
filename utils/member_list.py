import pandas as pd
import numpy as np
import os,sys

CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT,'..')
sys.path.append(ROOT)

def reveal_data_status(filename:str):
    try:
        status = ''
        if os.path.exists(filename):
            status = f'{filename} is already exists'        
        else:
            status = f'{filename} is invalid'
        return status
    
    except Exception as error:
        return error
    