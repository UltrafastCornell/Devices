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
        # Initialize PowerMeter base class
        Spectrometer.__init__(self)


        # Override Device.Load_Data() method
    def Load_Data(self, file_path = []):
        """Load centroid measurement as a Pandas data frame saved in centroid"""
        # Run parent method
        Device.Load_Data(self, file_path)
        
        for file_path in self.current_file_path:
            
            # Create empty array to hold text data read by csv reader
            txt_data = [];

            try:
                # Open file and read desired data. Append to txt_data array
                with open(file_path, 'r') as file:
                    
                    # Using csv reader, read in items in a row that do not include '', 'NA', and 'Hint'
                    myReader = csv.reader(file, delimiter='\t')
                    for row in myReader:
                        clean_row = []
                        for item in row:
                            if (not item == '' and not item == 'NA' and not item == 'Hint'):
                                clean_row.append(item);
                        txt_data.append(clean_row);
                    file.close()

            except:
                self.log.append(('FilePathError: ', file_path, ' is an invalid file path'))
                return
            
            # Convert text data to dataframe
            df = pd.DataFrame(data = txt_data[1:], columns = txt_data[0])

            # Collect columns correspond to centroid measurments of In Coupling, Single Pass, and Double Pass camers
            df_centroids = df[['Timestamp', '#1 MX [mm]', '#1 MY [mm]', '#2 MX [mm]', '#2 MY [mm]', '#4 MX [mm]', '#4 MY [mm]']]

            # Convert strings to numerical data
            df_numerical = df_centroids.drop('Timestamp', axis = 1).apply(lambda x: pd.to_numeric(x, errors='coerce'), axis = 1)

            # Create a Time column that contains the time of each data point in seconds
            Get_Time = lambda time: datetime.strptime(time, '%Y/%m/%d %H:%M:%S').timestamp()
            time = [Get_Time(time) - Get_Time(df_centroids['Timestamp'][0]) for time in df_centroids['Timestamp']]
            df_numerical['Time [s]'] = time

            # Get date to use as label. To be appended to date_array
            # df_numerical['Date'] = datetime.strptime(df_centroids['Timestamp'][0], '%Y/%m/%d %H:%M:%S').date();
            df_numerical['Date'] = df_centroids['Timestamp'].apply(lambda t:datetime.strptime(t, '%Y/%m/%d %H:%M:%S').date());

            # Define column names to use to rename data
            col_names = ['Time', 'Xc', 'Yc', 'Date'];

            # Rename column labels using specified column names. Add dataframe corresponding to each camera to a list.
            cam_df_list = [];
            cam_df_list.append(df_numerical[['Time [s]', '#1 MX [mm]', '#1 MY [mm]', 'Date']].rename(index = str, columns = {'Time [s]': col_names[0], '#1 MX [mm]': col_names[1], '#1 MY [mm]': col_names[2]}));
            cam_df_list.append(df_numerical[['Time [s]', '#2 MX [mm]', '#2 MY [mm]', 'Date']].rename(index = str, columns = {'Time [s]': col_names[0], '#2 MX [mm]': col_names[1], '#2 MY [mm]': col_names[2]}));
            cam_df_list.append(df_numerical[['Time [s]', '#4 MX [mm]', '#4 MY [mm]', 'Date']].rename(index = str, columns = {'Time [s]': col_names[0], '#4 MX [mm]': col_names[1], '#4 MY [mm]': col_names[2]}));

            # Create a list of camera names to use as super labels.
            cam_list = ['In Coupling', 'Single Pass', 'Double Pass'];

            # Concate dataframes organized by cameras
            df_total = pd.concat( cam_df_list, keys = cam_list, axis = 1 );

            # Add this data set to the rest of the data
            self.data += [df_total]
