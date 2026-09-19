import sys,os
import pandas as pd


def get_directories_():
    try:
        CURRENT = os.path.dirname(os.path.abspath(__file__))
        ROOT = os.path.join(CURRENT,"..")
        DATA = os.path.join(ROOT,"data")
        OUTPUT_DATA = os.path.join(ROOT,"output","ILLUMINATIAPP","data")
        
        
        
        print("CURRENT DIR: ",CURRENT)
        print("ROOT DIR: ",ROOT)
        print("App Data: ",DATA)
        print("Extracted App data: ",OUTPUT_DATA)
        
        
    except Exception as error:
        print("[x]: General Errors: \n",error)
        

if __name__ == "__main__":
    get_directories_()