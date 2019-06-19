# Import Camera base class
from ..Device import Device
from .Spectrometer import Spectrometer

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns



class Ando(Spectrometer):
    #   Helper functions for formatting and plotting
    #   data from Ocean Optics spectrometers
    


    def __init__(self):
        # Initialize PowerMeter base class
        Spectrometer.__init__(self)



    def Load_Data(self, file_path = []):
        """Load spectrum as a Pandas data frame"""

        # Run parent method
        Device.Load_Data(self, file_path)
        
        for file_path in self.current_file_path:
            try:
                df = pd.read_csv(file_path, skiprows = 3, delimiter = ',', names = ['Wavelength', 'Amplitude'], engine = 'c')
                #df = pd.read_csv(file, skiprows = 3, delimiter = ',', names = ['Wavelength', 'Amplitude'], 
                 #                error_bad_lines=False, skipfooter = 17, engine = 'python');
            except:
                print('FilePathError: invalid file path')
                self.log.append('FilePathError: invalid file path')

            df.drop(index = range(len(df) - 19, len(df)), inplace = True) # This drops all of the string information at the end of the file. Not sure if it is the same for every spectrometer setting.
            df = df.apply(pd.to_numeric, axis = 1)

            # Add this data set to the rest of the data
            self.data += [df]



    def Plot_Spectrum(self, same_axis = True):
        """Plot spectrum from Ando spectrum analyzer"""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        if same_axis:
            ax = self.Plot_Same_Axis()
        else:
            ax = self.Plot_Diff_Axis()

        plt.tight_layout()

        return ax



    def Plot_Same_Axis(self):
        '''Plot all recorded files on the same figure axis.'''

        # Create new figure
        fig, ax = plt.subplots(nrows = 1, ncols = 1, squeeze = False, figsize = (24, 12))
        
        # Color maps for plotting different sets of data
        color_list = ["blue", "green", "red", "purple", "orange"]
        
        data_index = 0
        for data in self.data:

            # Grab wavelength and amplitude from recorded data
            wavelength = data["Wavelength"]
            amplitude = data["Amplitude"]

            amplitude_linear = 10**(amplitude/10) / np.max(10**(amplitude/10))

            # Generate scatter plot of centroid data
            ax[0, 0].plot(wavelength, amplitude_linear, c=color_list[data_index%len(color_list)], lw = 4, label = 'File #' + str(data_index + 1))
            
            # Keeps track of number of data sets plotted
            data_index += 1

        # Set default labels
        plt.legend(loc='upper right')
        ax[0, 0].set_title('Ando Spectra')
        ax[0, 0].set_xlabel('Wavelength [nm]')
        ax[0, 0].set_ylabel('Amplitude [A.U.]')
            
        return ax



    def Plot_Diff_Axis(self):
        '''Plot all recorded files on their own axes.'''

        # Create new figure
        fig, ax = plt.subplots(nrows = len(self.data), ncols = 1, squeeze = False, figsize = (24, 6 * len(self.data)))
        
        # Color maps for plotting different sets of data
        color_list = ["blue", "green", "red", "purple", "orange"]
        
        data_index = 0
        for data in self.data:

            # Grab wavelength and amplitude from recorded data
            wavelength = data["Wavelength"]
            amplitude = data["Amplitude"]

            amplitude_linear = 10**(amplitude/10) / np.max(10**(amplitude/10))

            # Generate scatter plot of centroid data
            ax[data_index, 0].plot(wavelength, amplitude_linear, c=color_list[data_index%len(color_list)], lw = 4)
            
            # Set default labels
            ax[data_index, 0].set_title('File #' + str(data_index + 1))
            ax[data_index, 0].set_xlabel('Wavelength [nm]')
            ax[data_index, 0].set_ylabel('Amplitude [A.U.]')

            # Keeps track of number of data sets plotted
            data_index += 1

        return ax