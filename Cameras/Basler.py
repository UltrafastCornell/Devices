# Import Camera base class
from ..Device import Device
from .Camera import Camera

# Import packages for data analysis
import numpy as np
import pandas as pd

# Import packages for plotting
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import seaborn as sns

# Import packages for time data manipulation
from datetime import datetime

# Import package for reading csv file
import csv

class Basler(Camera):
    """Helper functions for formatting and plotting
    data from DataRay cameras"""
    
    def __init__(self):
        # Initialize camera base class
        Camera.__init__(self)



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



    def Normalize_By_Radius(self, Xr, Yr):
        """Normalize centroid measurement by the beam radius"""
    
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        self.data["Xc"] = self.data["Xc"]/Xr
        self.data["Yc"] = self.data["Yc"]/Yr        
        


    def Plot_Centroid(self, camera_list = ['In Coupling']):
        """Plot centroid as a function of time. A list of cameras to plot should be included. The list can contain 'In Coupling', 'Single Pass', and/or 'Double Pass'."""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        # Create new figure
        fig, ax = plt.subplots(nrows = len(camera_list), ncols = 1, squeeze=False, figsize=(12,8*len(camera_list)))
        
        # Color maps for plotting different sets of data
        cmaps = ["Blues", "Greens", "Reds", "Purples", "Oranges"]
        legend_color = ['Blue', 'Green', 'Red', 'Purple', 'Orange']
    
        points_from_end = 360

        data_index = 0
        for data in self.data:

            camera_index = 0
            for camera in camera_list:

                # Get time data
                Time = data[camera]['Time'][-points_from_end:] - data[camera]['Time'].iloc[-points_from_end]
            
                t_min = 0
                t_max = 3000
                # Grab centroid X and Y coordinates
                Xc = data[camera]["Xc"][-points_from_end:]#[t_min:t_max]
                Yc = data[camera]["Yc"][-points_from_end:]#[t_min:t_max]
            
                # Set scatter plot color based on element index
                color = Time#[t_min:t_max]

                # Generate scatter plot of centroid data
                s = ax[camera_index, 0].scatter(x=Xc, y=Yc, c = color, cmap = cmaps[data_index%len(cmaps)], edgecolor = 'k', lw = 0.5, s = 40, label = data[camera]['Date'][0])
            
                # # Create and label colorbar
                # cb = plt.colorbar(s)
                # cb.set_label('Time [s]')

                # Keeps track of number of cameras plotted
                camera_index += 1
            
            # Keeps track of number of data sets plotted
            data_index += 1

        for i in range(len(camera_list)):
            # Set default labels
            ax[i, 0].set_title(camera_list[i] + ' Beam Centroid')
            ax[i, 0].set_xlabel('$\mathrm{X_{c}}$ $\mathrm{[mm]}$')
            ax[i, 0].set_ylabel('$\mathrm{Y_{c}}$ $\mathrm{[mm]}$')
        
            # Create plot legend and label by date
            ax[i, 0].legend(loc='center left', bbox_to_anchor=(1, 0.5))
            leg = ax[i, 0].get_legend()
            for j in range(len(self.data)):
                leg.legendHandles[j].set_color(legend_color[j%len(legend_color)])

            # Set axis below plotted data
            ax[i,0].set_axisbelow(True);

        plt.tight_layout();

        return ax

    def Plot_Trace(self, camera_list = ['In Coupling']):
        """Plot X and Y coordinates as functions of time. A list of cameras to plot should be included. The list can contain 'In Coupling', 'Single Pass', and/or 'Double Pass'."""
        
        # Check if centroid data has been properly loaded
        if not self._Is_Data_Loaded(self.data):
            self.Load_Data()    

        # Create New figure
        fig, ax = plt.subplots(nrows = len(camera_list), ncols = 2, squeeze=False, figsize=(24,6*len(camera_list)))
        
        # Color maps for plotting different sets of data
        cmaps = ["Blues", "Greens", "Reds", "Purples", "Oranges"]
        legend_color = ['Blue', 'Green', 'Red', 'Purple', 'Orange']
    
        data_index = 0
        for data in self.data:

            camera_index = 0
            for camera in camera_list:

                # Get time data
                Time = data[camera]['Time']
            
                t_min = 0
                t_max = 3000
                # Grab centroid X and Y coordinates
                Xc = data[camera]["Xc"]#[t_min:t_max]
                Yc = data[camera]["Yc"]#[t_min:t_max]

                # # Generate scatter plot of centroid data
                # s = ax[camera_index, 0].scatter(x=Xc, y=Yc, c = color, cmap = cmaps[data_index%len(cmaps)], edgecolor = 'k', lw = 0.5, s = 40, label = data[camera]['Date'][0])
                # Plot X and Y coordinates as functions of time
                ax[camera_index,0].plot(Time, Xc, c = legend_color[data_index%len(legend_color)], lw = 2, label = data[camera]['Date'][0])
                ax[camera_index,1].plot(Time, Yc, c = legend_color[data_index%len(legend_color)], lw = 2, label = data[camera]['Date'][0])

                # Keeps track of number of cameras plotted
                camera_index += 1
            
            # Keeps track of number of data sets plotted
            data_index += 1

        for i in range(len(camera_list)):
            # Set default labels
            ax[i, 0].set_title(camera_list[i] + ' - X coordinate')
            ax[i, 0].set_xlabel('$\mathrm{Time}$ $\mathrm{[s]}$')
            ax[i, 0].set_ylabel('$\mathrm{X_{c}}$ $\mathrm{[mm]}$')
            
            ax[i, 1].set_title(camera_list[i] + ' - Y coordinate')
            ax[i, 1].set_xlabel('$\mathrm{Time}$ $\mathrm{[s]}$')
            ax[i, 1].set_ylabel('$\mathrm{Y_{c}}$ $\mathrm{[mm]}$')

            # Create plot legend and label by date
            ax[i, 1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
            leg = ax[i, 1].get_legend()
            for j in range(len(self.data)):
                leg.legendHandles[j].set_color(legend_color[j%len(legend_color)])

            # Set axis below plotted data
            ax[i,0].set_axisbelow(True);

        plt.tight_layout();

        return ax