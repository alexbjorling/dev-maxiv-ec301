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

    @attribute(label='Voltage', dtype=float, doc='Single voltage measurement', unit='V', format='1.3f')
    def voltage(self):
        return self.ec301.voltage

    @attribute(label='Current', dtype=float, doc='Single current measurement', unit='A', format='.3e')
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
    
    @command(dtype_in=float)
    def setPotential(self, pot):
        self.ec301.setPotential(pot)

    @command(dtype_in=float)
    def setCurrent(self, cur):
        self.ec301.setCurrent(cur)

    @command(dtype_in=str)
    def acquire(self, arg_list):
        arg_list = arg_list.strip()
        time, trigger = [eval(s) for s in arg_list.split()]
        self.ec301.acquire(time, trigger)

    @command(dtype_in=str)
    def potentialStep(self, arg_list):
        arg_list = arg_list.strip()
        t0, t1, E0, E1, trigger, full_bandwidth, return_to_E0 = [eval(s) for s in arg_list.split()]
        self.ec301.potentialStep(t0, t1, E0, E1, trigger, full_bandwidth, return_to_E0)

    @command(dtype_in=str)
    def potentialCycle(self, arg_list):
        arg_list = arg_list.strip()
        t0, E0, E1, E2, v, cycles, trigger = [eval(s) for s in arg_list.split()]
        self.ec301.potentialCycle(t0, E0, E1, E2, v, cycles, trigger)

    @command()
    def stop(self):
        self.ec301.stop()

    @command(dtype_out=(float,))
    def readout_t(self):
        t, E, I, aux, raw = self.ec301.readout()
        return t

    @command(dtype_out=(float,))
    def readout_E(self):
        t, E, I, aux, raw = self.ec301.readout()
        return E

    @command(dtype_out=(float,))
    def readout_I(self):
        t, E, I, aux, raw = self.ec301.readout()
        return I

    @command(dtype_out=(float,))
    def readout_aux(self):
        t, E, I, aux, raw = self.ec301.readout()
        return aux

    @command(dtype_out=(float,))
    def readout_raw(self):
        t, E, I, aux, raw = self.ec301.readout()
        return raw


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

