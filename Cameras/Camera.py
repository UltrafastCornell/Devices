# Import Device class from folder above
from ..Device import Device

class Camera(Device):
    """Class with functions specific to cameras"""

    def __init__(self):
        # Initialize Device base class
        Device.__init__(self)