# Import Camera base class
from ..Device import Device
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



    def Load_Data(self, file_path = []):
        """Load centroid measurement as a Pandas data frame saved in centroid"""

        Device.Load_Data(self, file_path)

        try:
            self.data = pd.read_excel(self.current_file_path)
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')
        
        # Get rid of spaces in column titles
        self.data = self.data.rename(index=str, columns={" Xc ": "Xc", " Yc ": "Yc"})


    
    def Normalize_By_Radius(self, Xr, Yr):
        """Normalize centroid measurement by the beam radius"""

        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Centroid()    

        self.data["Xc"] = self.data["Xc"]/Xr
        self.data["Yc"] = self.data["Yc"]/Yr        



    def Plot_Centroid(self):
        """Plot centroid as a function of time"""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    
        
        # Grab centroid X and Y coordinates
        Xc = self.data["Xc"]
        Yc = self.data["Yc"]

        # Set scatter plot color based on element index
        color = self.data.index
           
        # Create new figure
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])

        # Generate scatter plot of centroid data
        s = ax.scatter(x = Xc, y = Yc, c=np.linspace(0,1,len(color)), cmap='Spectral')
       
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