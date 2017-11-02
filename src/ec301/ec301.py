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
                        min_value=-15.0, max_value=15.0,
                        doc="current voltage")

    currrent = attribute(label="Current", 
                        dtype=float,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ, # or READ_WRITE
                        unit="A",
                        format=".4e",
                        min_value=-1.0, max_value=1.0,
                        doc="current current")

    idstring = attribute(label="ID", 
                        dtype=str,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ, # or READ_WRITE
                        doc="device ID string")

    error = attribute(label="Error", 
                        dtype=str,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ, # or READ_WRITE
                        doc="last error message")

    running = attribute(label="Running",
                        dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ, # or READ_WRITE
                        doc="is the device acquiring/scanning?")

    mode = attribute(label="Mode",
                        dtype=enum, #FIXME
                        enum_labels=('POTENTIOSTAT', 'GALVANOSTAT', 'ZRA')
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE
                        doc="control loop mode")

    enabled = attribute(label="Enabled",
                        dtype=bool,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE
                        doc="is the cell under device control?")

    irange = attribute(label="Range",
                        dtype=int,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE
                        doc="current range as log(range/A)")

    autorange = attribute(label="Autorange",
                        dtype=bool
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE
                        doc="current range automatically set?")

    averaging = attribute(label="Averaging",
                        dtype=int,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE
                        doc="number of 4 us samples averaged in each data point")

    bandwidth = attribute(label="Bandwidth",
                        dtype=int,
                        display_level=DispLevel.OPERATOR,
                        access=AttrWriteType.READ_WRITE
                        doc="control loop bandwidth as log(bw/Hz)")


    ### Read methods for the read only attributes ###

    def read_voltage(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_voltage')

    def read_current(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_current')

    def read_id(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_id')
 
     def read_error(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_error')

    def read_running(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_running')

    ### Read/write methods for the read/write attributes ###

    def read_mode(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_mode')

    def write_mode(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at write_mode')

    def read_enabled(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_enabled')

    def write_enabled(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at write_enabled')

    def read_irange(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_irange')

    def write_irange(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at write_irange')

    def read_autorange(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_autorange')

    def write_autorange(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at write_autorange')

    def read_averaging(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_averaging')

    def write_averaging(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at write_averaging')

    def read_bandwidth(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at read_bandwidth')

    def write_bandwidth(self):
        try:
            raise NotImplementedError
        except:
            self.set_state(PyTango.DevState.FAULT)
            self.set_status('Device failed at write_bandwidth')

    ### Commands ###
    
    @command()
    def setPotential(self, pot):
        raise NotImplementedError
        return True

    @command()
    def setCurrent(self, cur):
        raise NotImplementedError
        return True

    @command()
    def acquire(self, time=1.0, trigger=False):
        raise NotImplementedError
        return True

    @command()
    def potentialStep(self, t0=1, t1=1, E0=0, E1=1, trigger=False, 
                full_bandwidth=True, return_to_E0=True):
        raise NotImplementedError
        return True

    @command()
    def potentialCycle(self, t0=1, E0=.2, E1=1, E2=0, 
                v=.100, cycles=1, trigger=False):
        raise NotImplementedError
        return True

    @command()
    def stop(self):
        raise NotImplementedError
        return True

    @command()
    def readout(self):
        raise NotImplementedError
        return True


    ### Other stuff ###

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


def main():
    server_run((EC301DS,))

if __name__ == "__main__":
    main()


