# Import Camera base class
from .PowerMeter import PowerMeter

class Coherent(PowerMeter):
    #   Helper functions for formatting and plotting
    #   data from Coherent power meters
    
    def __init__(self):
        # Initialize PowerMeter base class
        PowerMeter.__init__(self)

        # Measured data as a pandas DataFrame
        self.data = None


    
    # Load  measurement as a Pandas data frame
    # saved in 
    def Load_Centroid(self, file_path = False):
        # Get the file path of the  measurement
        if not file_path:
            # Prompt user to locate the file path
            file_path = self._Get_File_Path()

        try:
            #  = pd.read_excel(file_path)
            pass
        except:
            print('FilePathError: invalid file path')
            self.log.append('FilePathError: invalid file path')
