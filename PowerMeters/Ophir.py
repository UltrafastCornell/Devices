# Import Camera base class
from .PowerMeter import PowerMeter

# Import packages for data analysis
import numpy as np
import pandas as pd
import csv
from itertools import compress

# Import packages for plotting
import matplotlib.pyplot as plt
import seaborn as sns

class Ophir(PowerMeter):
    #   Helper functions for formatting and plotting
    #   data from Ophir power meters
    
    def __init__(self):
        # Initialize PowerMeter base class
        PowerMeter.__init__(self)

        # Measured data as a pandas DataFrame
        self.power = None


    # Load  measurement as a Pandas data frame
    def Load_Power(self, file_path = False):
        """Load power data from StarLab (Ophir) software. Returns the header separated into sections and a Pandas dataframe of power data."""
    
        def Section_Header(header):
            ### Clean up header by sectioning into sublists
            # split header where empty lists occur
            # create new sublist when find empty element. Step when get to First Pulse Arrived string
            bool_list = [];
            sub_list = [];
            sectioned_header = [];
            units_list = [];
            meters_list = [];
    
            for row in header:
                if not row or '---' in row[0]: # if row is empty
                    if sub_list: # if sub_list is not empty append sub_list to sorted_list and reset sub_list
                        sectioned_header.append(sub_list)
                        sub_list = [];
                else:
                    sub_list.append(row[0]); # if row is not empty append to sub_list
                    if 'Units' in row[0]:
                        units_list.append(row[0].split(':')[1])
                    if 'Name' in row[0]:
                        meters_list.append(row[0].split(':')[1])
    
            sectioned_header.append(sub_list) # append last collected sub_list to sorted_list
        
            return sectioned_header, units_list, meters_list
    
        def Clean_Data(data):
            ### Prepare data to construct dataframe.
            # clean up labels in first row of data.
            stripped_labels = [item.strip() for item in data[0]]
            channel_labels = [item for item in stripped_labels if 'Channel' in item]
            time_labels = ['Timestamp ' + item.split()[1] for item in stripped_labels if 'Channel' in item]
            column_labels = time_labels + channel_labels
    
            # clean up numerical data in rest of data.
            numeric_data = data[1:]
            power_array = [];
            time_array = [];
    
            for i in range(len(channel_labels)):
                power_list = [];
                time_list = [];
                for j in range(len(numeric_data[:,i+1])):
                    # try to convert string to float value. If error, then the string is blank space and pass.
                    try:
                        power_list.append(float(numeric_data[j,i+1]))
                        time_list.append(float(numeric_data[j,0]))
                    except:
                        pass
        
                power_array.append(power_list);
                time_array.append(time_list);
        
            numerical_data = np.transpose(time_array + power_array)
        
            return column_labels, numerical_data
    
        # Get the file path of the  measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()
        
        ### Load and read csv file.
        file = [];
        
        try:
            with open(file_path, "r") as csvfile:
                # csvfile.seek(character_number) # reset cursor to specified character of csvfile
                # csvfile.read(character_number) # read to specified character number of csvfile
                myReader = csv.reader(csvfile, delimiter='\t')
                for row in myReader:
                    file.append(row);
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')

        ### Find beginning of data using 'Timestamp' string to split file into header and data.
        bool_list = [];
    
        for row in file:
            if not row: # if row is empty
                bool_list.append(False);
            else:
                bool_list.append('Timestamp' in row[0]);
    
        # compress finds row that contains 'Timestamp' string.
        data_start = list(compress(range(len(bool_list)), bool_list))[0] # Compress boolean array down to indices that contain True values.
    
        # split file into header and data
        header = file[:data_start];
        data = np.array(file[data_start:])[:,0:3];
    
        ### Section header
        sectioned_header, units_list, meters_list = Section_Header(header);
    
        ### Prepare data to construct dataframe
        column_labels, numerical_data = Clean_Data(data);
    
        ### Construct dataframe
        df = pd.DataFrame(columns = column_labels, data = numerical_data)
    
        self.power = df;
        self.header = sectioned_header;
        self.meters = meters_list;
        self.units = units_list;