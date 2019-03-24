# Import Camera base class
from .Camera import Camera

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

class DataRay(Camera):
    """Helper functions for formatting and plotting
    data from DataRay cameras"""
    
    def __init__(self):
        # Initialize camera base class
        Camera.__init__(self)
        
        # Measured centroid data as a pandas DataFrame
        self.centroid = None



    def Load_Centroid(self, file_path = False):
        """Load centroid measurement as a Pandas data frame saved in centroid"""

        # Get the file path of the centroid measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()
            print('Setting file path to: ', file_path)

        try:
            self.centroid = pd.read_excel(file_path)
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')
        
        # Get rid of spaces in column titles
        self.centroid = self.centroid.rename(index=str, columns={" Xc ": "Xc", " Yc ": "Yc"})



    def Plot_Centroid(self):
        """Plot centroid as a function of time"""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.centroid):
            self.Load_Centroid()    

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