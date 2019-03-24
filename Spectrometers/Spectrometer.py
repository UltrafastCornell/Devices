# Import Device class from folder above
from ..Device import Device

class Spectrometer(Device):
    """Class with functions specific to spectrometers"""

    def __init__(self):
        # Initialize Device base class
        Device.__init__(self)