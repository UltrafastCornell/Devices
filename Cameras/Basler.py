# Import Camera base class
from ..Device import Device
from .Camera import Camera

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

class Basler(Camera):
    """Helper functions for formatting and plotting
    data from DataRay cameras"""
    
    def __init__(self):
        # Initialize camera base class
        Camera.__init__(self)

		# Measured data as a pandas DataFrame
        self.data = None


    # Override Device.Load_Data() method
    def Load_Data(self, file_path = []):
        """Load centroid measurement as a Pandas data frame saved in centroid"""
        # Run parent method
        Device.Load_Data(self, file_path)

        try:
            # Read Pandas dataframe from a csv
            df = pd.read_csv(self.current_file_path, delimiter='\t', lineterminator='\n')
            
            # Drop unnecessary columns
            if '\r' in df.columns:
                df.drop(['\r'], axis = 1, inplace = True)
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')
        
        # Rename centroid labels
        df = df.rename(index=str, columns={"Mx All [px]": "Xc", "My All [px]": "Yc"})
        
        # Choos a name for this data set
        data_name = self.current_file_path.split("/")[-1].split(".")[0]     
        
        # Add data_name as a super header
        df.columns = pd.MultiIndex.from_product([[data_name], list(df.columns)])

        # Add this data set to the rest of the data
        self.data = pd.concat([self.data, df], axis = 1)


    
    def Normalize_By_Radius(self, Xr, Yr):
        """Normalize centroid measurement by the beam radius"""
    
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.centroid):
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
        