import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# tkinter enables file browsing
import tkinter as tk
from tkinter import filedialog

class WinCamD_LCM:
    #   Helper functions for formatting and plotting
    #   data from the DataRay WinCamD-LCM
    
    def __init__(self):
        # Measured centroid data as a pandas DataFrame
        self.centroid = None

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


    
    # Load centroid measurement as a Pandas data frame
    # saved in centroid
    def Load_Centroid(self, file_path = False):
        # Get the file path of the centroid measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()

        try:
            self.centroid = pd.read_excel(file_path)
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')
        
        # Get rid of spaces in column titles
        self.centroid = self.centroid.rename(index=str, columns={" Xc ": "Xc", " Yc ": "Yc"})



    # Check if the user has loaded centroid data
    def Check_For_Centroid_Data(self):
        try:
            self.centroid == None
        except:
            # The user has loaded centroid data
            self.log.append("Check for centroid data passed")
        else:
            # The user has not loaded centroid data
            self.log.append("Requesting centroid data")
            self.Load_Centroid()



    # Plot centroid as a function of time
    def Plot_Centroid(self):
        self.Check_For_Centroid_Data()

        # Create new figure
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])

        # Grab centroid X and Y coordinates
        Xc = self.centroid["Xc"]
        Yc = self.centroid["Yc"]

        # Set scatter plot color based on element index
        color = self.centroid.index

        # Generate scatter plot of centroid data
        s = ax.scatter(x = Xc, y = Yc, c=color, cmap='Spectral')
       
        # Set default labels
        ax.set_title('Beam Centroid')
        ax.set_xlabel('$X_{c}$ $[\mu m]$')
        ax.set_ylabel('$Y_{c}$ $[\mu m]$')

        # Set axis below plotted data
        ax.set_axisbelow(True)

        # Create and label colorbar
        cb = plt.colorbar(s)
        cb.set_label('Time [s]')

        return ax