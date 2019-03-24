# Import Device class from folder above
from ..Device import Device

class PowerMeter(Device):
    """Class with functions specific to powermeters"""

    def __init__(self):
        # Initialize Device base class
        Device.__init__(self)