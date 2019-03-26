# Import Camera base class
from .PowerMeter import PowerMeter

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

class Coherent(PowerMeter):
    #   Helper functions for formatting and plotting
    #   data from Coherent power meters
    
    def __init__(self):
        # Initialize PowerMeter base class
        PowerMeter.__init__(self)

        # Measured data as a pandas DataFrame
        self.data = None


    
    # Load  measurement as a Pandas data frame
    # saved in 
    def Load_Data(self, file_path = []):
        # Override Device.Load_Data() method
        Device.Load_Data(self, file_path)

        try:
            #  = pd.read_excel(self.current_file_path)
            pass
        except:
            print('FilePathError: invalid file path')

            self.log.append('FilePathError: invalid file path')
