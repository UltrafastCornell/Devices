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
        # Initialize PowerMeter base class
        Spectrometer.__init__(self)
        
        # Measured data as a pandas DataFrame
        self.spectrum = None
