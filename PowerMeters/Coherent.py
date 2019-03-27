# Import Camera base class
from ..Device import Device
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


    
    # Load  measurement as a Pandas data frame
    def Load_Data(self, file_path = []):
        # Override Device.Load_Data() method
        Device.Load_Data(self, file_path)

        try:
            data = pd.read_csv('1603 compressor warmup.csv', delimiter = ',', header = 2);
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')

        # Convert Timestamp column to DateTime object if it isn't already
        if type(data['Timestamp'][0]) is not pd.Timestamp:
            data['Timestamp'] = data['Timestamp'].apply(lambda x: pd.to_datetime(''.join(x.split('-')), infer_datetime_format = True));
        data['Time (s)'] = data['Timestamp'].apply(lambda x: (x - data['Timestamp'][0]).total_seconds());

        self.data = data;

    def Plot_Power(self):
        """Plot centroid as a function of time"""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    
        
        # Get time (s) and power from dataframe
        time = data['Time (s)'];
        power = data['0246D17R:Watts'];

        # Set figure format
        sns.set_context('notebook',font_scale=1.5);

        # Create new figure and axis object
        fig, ax = plt.subplots(figsize=(10,6));

        # Plot data
        ax.plot(time, power)

        # Set default labels
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Power (W)')

        # Turn grid on for axis
        ax.grid()

        # Call plot tight layout
        plt.tight_layout()

        return ax
