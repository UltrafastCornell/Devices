# tkinter enables file browsing
import tkinter as tk
from tkinter import filedialog

class Device:
    """Base class of devices"""
    
    def __init__(self):
        # Dataframe containing all of the device data
        self.data = []
        
        # File path of data
        self.current_file_path = []

        # Information log
        self.log = []
    
    

    def _Get_File_Path(self):
        """Open dialogue box that prompts the user to select a file path"""

        # Assign handel to tkinter root window
        root = tk.Tk()

        # Bring root window above other windows
        root.attributes("-topmost", True)
        
        # String containing the file path
        file_path = filedialog.askopenfilename()

        # Destroy the root window
        root.destroy()

        return file_path



    def _Is_Data_Loaded(self, data):
        """Check if the user has loaded data"""

        try:
            data == []

        except:
            # The user has loaded the data
            self.log.append("Check for loaded data passed")
            return True

        else:
            # The user has not loaded the data
            self.log.append("Check for loaded data failed")
            return False



    def Load_Data(self, file_path = []):
        """Load device data to be analyzed"""

        # Get the file path of the centroid measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()

        self.current_file_path = file_path
