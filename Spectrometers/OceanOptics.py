# Import Camera base class
from ..Device import Device
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
        # Initialize Spectrometer base class
        Spectrometer.__init__(self)




    ### New code taken and editted from Ando spectrometer class
    def Load_Data(self, file_path = []):
        """Load spectrum as a Pandas data frame"""

        # Run parent method
        Device.Load_Data(self, file_path)
        
        caps_per_file = []
        for file_path in self.current_file_path:
            try:
                with open(file_path) as f:
                    first_line = f.readline()
                capture_names = first_line.split(sep=None)
                
                num_captures = len(capture_names)
                caps_per_file += [num_captures]
                
                name_list = []
                for i in range(num_captures):
                    name_list += ['Wavelength ' + str(i), 'Amplitude ' + str(i)]
                
                df = pd.read_csv(file_path, skiprows = 1, delimiter = '\t', names = name_list, index_col = False)
            except:
                print('FilePathError: invalid file path')
                self.log.append('FilePathError: invalid file path')

            # Add this data set to the rest of the data
            self.data += [df]
            self.caps_per_file = caps_per_file



    def Plot_Spectrum(self, same_axis = True):
        """Plot spectrum from Ocean Optics spectrometers. Plot all recorded files on different figure axis. Each file can have multiple captures which are plotted on the same axis."""
        
        # Check if data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        ###
        # Create new figure
        
        fig, ax = plt.subplots(nrows = len(self.data), ncols = 1, squeeze = False, figsize = (24, 6*len(self.data)))

        # Color maps for plotting different sets of data
        color_list = ["blue", "green", "red", "purple", "orange"]

        data_index = 0
        for data in self.data:

            # Grab wavelength and amplitude from recorded data
            for i in range(self.caps_per_file[data_index]):
                wavelength = data["Wavelength " + str(i)]
                amplitude = data["Amplitude " + str(i)]

                # Plot linear spectrum (Not scaled by power scaling of spectrometers--this would be different for each spectrometer)
                ax[data_index, 0].plot(wavelength, amplitude, c=color_list[i%len(color_list)], lw = 4, label = 'Capture #' + str(i))
            
            ax[data_index, 0].legend(loc='upper right')
            
            # Set default labels
            ax[data_index, 0].set_title('File #' + str(data_index + 1))
            ax[data_index, 0].set_xlabel('Wavelength [nm]')
            ax[data_index, 0].set_ylabel('Amplitude [A.U.]')
            
            # Keeps track of number of data sets plotted
            data_index += 1

        # Set default labels
        ax[0, 0].set_xlabel('Wavelength [nm]')
        ax[0, 0].set_ylabel('Amplitude [A.U.]')    
        ###

        plt.tight_layout()

        return fig, ax
    