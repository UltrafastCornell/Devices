# Import Camera base class
from .Spectrometer import Spectrometer

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

class OceanOptics(Spectrometer):
    #   Helper functions for formatting and plotting
    #   data from Ocean Optics spectrometers
    
    def __init__(self):
<<<<<<< HEAD
        # Measured data as a pandas DataFrame
        self.data = None

        # Information log
        self.log = []

    
    
    # Open dialogue box that prompts the user to 
    # select a file path
    def _Get_File_Path(self):
        # Assign handel to tkinter root window
        root = tk.Tk()

        # Bring root window above other windows
        root.attributes("-topmost", True)
        
        # String containing the file path
        file_path = filedialog.askopenfilename()

        # Destroy the root window
        root.destroy()

        return file_path


    
    # Load  measurement as a Pandas data frame
    # saved in 
    def Load_Centroid(self, file_path = False):
        # Get the file path of the  measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()

        try:
            #  = pd.read_excel(file_path)
            pass
        except:
            print('FilePathError: invalid file path')
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
        # Initialize PowerMeter base class
        Spectrometer.__init__(self)
        
        # Measured data as a pandas DataFrame
        self.spectrum = None
>>>>>>> bff4e1da8940225505536eb860ad721b23e21b5c
