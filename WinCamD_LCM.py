import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import tkinter as tk
from tkinter import filedialog

class WinCamD_LCM:
    #   Helper functions for formatting and plotting
    #   data from the DataRay WinCamD-LCM
    
    def __init__(self):
        self.centroid

    
    
    # Open dialogue box that prompts the user to 
    # select a file path
    def _Get_File_Path(self):
        # Assign handel to tkinter root window
        root = tk.Tk()

        # Bring root window above other windows
        root.attributes("-topmost", True)
        
        # String containing the file path
        file_path = filedialog.askopenfilename()

        # Destroy the root window
        root.destroy()

        return file_path


    
    # Load centroid measurement as a Pandas data frame
    # saved in centroid
    def Load_Centroid_Measurement(self, file_path = False):
        # Get the file path of the centroid measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()

        try:
            self.centroid = pd.read_excel(file_path)
        except:
            print('FilePathError: invalid file path')

        self.centroid.rename(index=str, columns={" Xc ": "Xc", " Yc ": "Yc"})

        return self.centroid




