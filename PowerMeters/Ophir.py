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
<<<<<<< HEAD
            self.log.append('FilePathError: invalid file path')
        


    # Check if the user has loaded centroid data
    def Check_For_Data(self):
        try:
            # data to check == None
            pass
        except:
            # The user has loaded centroid data
            self.log.append("Check for data passed")
        else:
            # The user has not loaded centroid data
            self.log.append("Requesting data")
            # Load function here



    # Plot as a function of time
    def Plot(self):
        self.Check_For_Data()
=======
            self.log.append('FilePathError: invalid file path')      
>>>>>>> bff4e1da8940225505536eb860ad721b23e21b5c
