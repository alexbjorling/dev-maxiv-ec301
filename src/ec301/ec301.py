# Device library import
import ec301lib

# Tango imports
from PyTango import AttrWriteType, DispLevel
from PyTango.server import Device, DeviceMeta, attribute, command, server_run,  device_property
import PyTango

class EC301DS(Device):
    """ An SRS EC301 device

       Device States Description:
    #
    #   DevState.ON :     The device is in operation
    #   DevState.INIT :   Initialisation of the communication with the device and initial configuration
    #   DevState.FAULT :  The Tango Device is not able to serve the request from/to this device.
    #                     Possible cause :
    #                     - Wrong Ip address : unable to communicate with the device
    #                     - The device doesn't respond : not wired to the network or powered off
    #                     - Failure loading library
    #   DevState.Moving :  The Tango Device is performing a movement.
    """
    __metaclass__ = DeviceMeta


    ### Properties ###
    Host = device_property(dtype=str, default_value="b-nanomax-ec301-0", doc="hostname")
    Port = device_property(dtype=int, default_value=1680)


    ### Attributes ###
    voltage = attribute(label="Voltage", 
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ, # or READ_WRITE
                        unit="V",
                        format="4.2f",
                        min_value=0.0, max_value=110.0,
                        min_alarm=-5.0, max_alarm=110.0,
                        min_warning=-5.0, max_warning=105.0,
                        fget="get_voltage",
                        doc="current voltage")

    # HOW DOES THIS WORK?
    def get_device_properties(self, cls=None):
        """Patch version of device properties.

       Set properties at instance level in lower case.
       """
        Device.get_device_properties(self, cls)
        for key, value in self.device_property_list.items():
           setattr(self, key.lower(), value[2])
           
    # Device methods
    def init_device(self):
        """Instantiate device object, do initial instrument configuration."""
        self.set_state(PyTango.DevState.INIT)
        
        try:
            self.get_device_properties()
            self.ec301 = ec301lib.EC301(host=self.Host, port=self.Port)
        
        except PyTango.DevFailed or PIe816Exception:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at init')
        
        self.set_state(PyTango.DevState.ON)
    
    # DO I NEED THIS?
    def always_executed_hook(self):
        pass


    ### Read/write methods for the attributes ###

    def get_voltage(self):
        try:
            return self.pilib.get_voltage(self.axis)
        except PyTango.DevFailed or PIe816Exception:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at get_voltage')
 

    ### Commands ###
    
    @command()
    def setPotential(self):
        raise NotImplementedError
        return True
        
def main():
    server_run((EC301DS,))

if __name__ == "__main__":
    main()


