# TODO:
#   * we need to interface ec301.running through some state getter
#   * returning data
#   * enums (below)
#   * other questionmarks below

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

    @attribute(label='Voltage', dtype=float, doc='Single voltage measurement', unit='V')
    def voltage(self):
        return self.ec301.voltage

    @attribute(label='Current', dtype=float, doc='Single current measurement', unit='A')
    def current(self):
        return self.ec301.current

    @attribute(label='ID', dtype=str, doc='Device ID string')
    def id(self):
        return self.ec301.id

    @attribute(label='Error', dtype=str, doc='Last error message')
    def error(self):
        return self.ec301.error

    @attribute(label='Running', dtype=bool, doc='acquiring/scanning')
    def running(self):
        return self.ec301.running

    ## How do these enums work?
    @attribute(label='Mode', dtype=str, doc='Control mode')
    def mode(self):
        return self.ec301.mode

    @mode.write
    def mode(self, mod):
        self.ec301.mode = mod

    @attribute(label='Enabled', dtype=bool, 
        doc='Cell enabled? Querying gives false if the front panel switch is out.')
    def enabled(self):
        return self.ec301.enabled

    @enabled.write
    def enabled(self, stat):
        self.ec301.enabled = stat

    @attribute(label='I Range', dtype=int, doc='Current range as log(range/A)')
    def Irange(self):
        return self.ec301.Irange

    @Irange.write
    def Irange(self, rng):
        self.ec301.Irange = rng

    @attribute(label='E Range', dtype=int, doc='Potential range (2, 5, or 15)', unit='V')
    def Erange(self):
        return self.ec301.Erange

    @Erange.write
    def Erange(self, rng):
        self.ec301.Erange = rng

    @attribute(label='Autorange', dtype=bool, doc='Autorange on/off')
    def autorange(self):
        return self.ec301.autorange

    @autorange.write
    def autorange(self, val):
        self.ec301.autorange = val

    @attribute(label='Averaging', dtype=int, doc='Sample averaging')
    def averaging(self):
        return self.ec301.averaging

    # should perhaps be an enum
    @averaging.write
    def averaging(self, avg):
        self.ec301.averaging = avg

    @attribute(label='Bandwidth', dtype=int, doc='Control loop bandwidth as log(bw/Hz)')
    def bandwidth(self):
        return self.ec301.bandwidth

    @bandwidth.write
    def bandwidth(self, bw):
        self.ec301.bandwidth = bw

    @attribute(label='I lowpass 10kHz', dtype=bool, doc='Enables 10 kHz low-pass filter in front of I ADC')
    def Ilowpass(self):
        return self.ec301.Ilowpass

    @Ilowpass.write
    def Ilowpass(self, val):
        self.ec301.Ilowpass = val

    @attribute(label='E lowpass 10kHz', dtype=bool, doc='Enables 10 kHz low-pass filter in front of E ADC')
    def Elowpass(self):
        return self.ec301.Elowpass

    @Elowpass.write
    def Elowpass(self, val):
        self.ec301.Elowpass = val

    @attribute(label='Compliance limit', dtype=float, doc='Limit on the compliance voltage', unit='V')
    def compliance_limit(self):
        return self.ec301.compliance_limit

    @compliance_limit.write
    def compliance_limit(self, val):
        self.ec301.compliance_limit = val


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

    # Can this return many arrays or does it have to be split into many commands?
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

