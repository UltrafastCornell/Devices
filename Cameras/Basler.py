# Import Camera base class
from ..Device import Device
from .Camera import Camera

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

# Import packages for time data manipulation
from datetime import datetime


class Basler(Camera):
    """Helper functions for formatting and plotting
    data from DataRay cameras"""
    
    def __init__(self):
        # Initialize camera base class
        Camera.__init__(self)

        self.data = None

    # Override Device.Load_Data() method
    def Load_Data(self, file_path = []):
        """Load centroid measurement as a Pandas data frame saved in centroid"""
        # Run parent method
        Device.Load_Data(self, file_path)

        try:
            # Read Pandas dataframe from a csv
            df = pd.read_csv(self.current_file_path, delimiter='\t', lineterminator='\n')
            
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')
            return
        
        # Drop unnecessary columns
        if '\r' in df.columns:
            df.drop(['\r'], axis = 1, inplace = True)

        # Rename centroid labels
        df = df.rename(index=str, columns={"Mx All [px]": "Xc", "My All [px]": "Yc"})
        
        # Create a Time column that contains the time of each data point in seconds
        Get_Time = lambda time: datetime.strptime(time, '%Y/%m/%d %H:%M:%S.%f').timestamp()
        time = [Get_Time(time) - Get_Time(df['TimeStamp'][0]) for time in df['TimeStamp']]
        df['Time'] = time
        
        # Choos a label for this data set
        data_label = self.current_file_path.split("/")[-1].split(".")[0]     
        
        # Add data_label as a super header
        df.columns = pd.MultiIndex.from_product([[data_label], list(df.columns)])
        
        # Add this data set to the rest of the data
        self.data = pd.concat([self.data, df], axis = 1)#, ignore_index = True)#.reindex(df.index)



    @property
    def data_labels(self):
        """Return a list of data labels"""

        # Check if data is loaded and return a list of labels
        if self._Is_Data_Loaded(self.data):
            return list(self.data.columns.levels[0])
        else:
            return []
    


    def Normalize_By_Radius(self, Xr, Yr):
        """Normalize centroid measurement by the beam radius"""
    
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        self.data["Xc"] = self.data["Xc"]/Xr
        self.data["Yc"] = self.data["Yc"]/Yr        
        


    def Plot_Centroid(self):
        """Plot centroid as a function of time"""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        # Create new figure
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        
        # Color maps for plotting different sets of data
        cmaps = ["Blues", "Greens", "Reds", "Purples", "Oranges"]
        
        for data_label in self.data_labels:
            # The current data set
            data = self.data[data_label]

            # Keeps track of number of data sets plotted
            data_index = self.data_labels.index(data_label)
            
            # Get time data
            Time = data['Time']
            
            t_min = 0
            t_max = 3000
            # Grab centroid X and Y coordinates
            Xc = data["Xc"]#[t_min:t_max]
            Yc = data["Yc"]#[t_min:t_max]
            
            # Set scatter plot color based on element index
            color = data.index#[t_min:t_max]

            # Generate scatter plot of centroid data
            s = ax.scatter(x = Xc, y = Yc, c=color, cmap=cmaps[data_index%len(cmaps)])
            
            # Create and label colorbar
            cb = plt.colorbar(s)
            cb.set_label('Time [s]')
            
        # Set default labels
        ax.set_title('Beam Centroid')
        ax.set_xlabel('$X_{c}$ $[\mu m]$')
        ax.set_ylabel('$Y_{c}$ $[\mu m]$')

        # Set axis below plotted data
        ax.set_axisbelow(True)

        return ax