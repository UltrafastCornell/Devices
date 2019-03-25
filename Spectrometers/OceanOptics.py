# Import Camera base class
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
<<<<<<< HEAD

=======
>>>>>>> 32183d11fe792fc4f2ae58c9ae07c987fe48c32b
        # Initialize PowerMeter base class
        Spectrometer.__init__(self)
        
        # Measured data as a pandas DataFrame
        self.spectrum = None
