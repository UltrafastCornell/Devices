# Import Camera base class
from .PowerMeter import PowerMeter

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

class Ophir(PowerMeter):
    #   Helper functions for formatting and plotting
    #   data from Ophir power meters
    
    def __init__(self):
        # Initialize PowerMeter base class
        PowerMeter.__init__(self)

        # Measured data as a pandas DataFrame
        self.power = None


    
    # Load  measurement as a Pandas data frame
    # saved in 
    def Load_Power(self, file_path = False):
        """Load and plot specified power data."""
        
        # Get the file path of the  measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()

        try:
            # self.power = 
            #  = pd.read_excel(file_path)
            pass
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')      

