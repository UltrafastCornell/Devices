# Import Camera base class
from .Spectrometer import Spectrometer

class OceanOptics(Spectrometer):
    #   Helper functions for formatting and plotting
    #   data from Ocean Optics spectrometers
    
    def __init__(self):
        # Initialize PowerMeter base class
        Spectrometer.__init__(self)
        
        # Measured data as a pandas DataFrame
        self.spectrum = None
