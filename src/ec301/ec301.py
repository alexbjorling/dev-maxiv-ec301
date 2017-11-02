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

    @attribute(label='Voltage', dtype=float, doc='Single voltage measurement'):
    def voltage(self):
        return self.ec301.voltage

    @attribute(label='Current', dtype=float, doc='Single current measurement'):
    def current(self):
        return self.ec301.current

    @attribute(label='ID', dtype=str, doc='Device ID string'):
    def id(self):
        return self.ec301.id

    @attribute(label='Error', dtype=str, doc='Last error message'):
    def error(self):
        return self.ec301.error

    @attribute(label='Running', dtype=bool, doc='acquiring/scanning'):
    def running(self):
        return self.ec301.running

    @attribute(label='Mode', dtype=enum, doc='Control mode', ## FIXME
            enum_labels=('POTENTIOSTAT', 'GALVANOSTAT', 'ZRA')):
    def mode(self):
        return self.ec301.mode

    @mode.write
    def mode(self, mod):
        return self.ec301.mode(mod)




## STILL TO DO:
    # ### Cell enabled? Querying gives false if the front panel switch is out.
    # @property
    # def enabled(self):
    #     return bool(int(self._query('cellon?')))

    # @enabled.setter
    # def enabled(self, state):
    #     assert state in [0, 1, True, False]
    #     self._query('ceenab %d' % int(state))

    # ### Current range as log(range/A)
    # @property
    # def range(self):
    #     return self.RANGE_MAP[int(self._query('irange?'))]

    # @range.setter
    # def range(self, rng):
    #     assert rng in self.RANGE_MAP.values()
    #     if self.autorange:
    #         self.autorange = False
    #     target = reversed_dict(self.RANGE_MAP)[rng]
    #     self._query('irange %d' % target)

    # ### Autorange on/off
    # @property
    # def autorange(self):
    #     return bool(int(self._query('irnaut?')))

    # @autorange.setter
    # def autorange(self, val):
    #     assert val in [0, 1, True, False]
    #     if not self.mode == 'POTENTIOSTAT':
    #         self.mode = 'POTENTIOSTAT'
    #     self._query('irnaut %d' % int(val))

    # ### Sample averaging
    # @property
    # def averaging(self):
    #     return 2**int(self._query('avgexp?'))

    # @averaging.setter
    # def averaging(self, avg):
    #     assert avg in 2**np.arange(8+1, dtype=int)
    #     val = int(np.log2(avg))
    #     self._query('avgexp %d' % val)
    #     time.sleep(.030) # The manual specifies this.

    # ### Control loop bandwidth
    # @property
    # def bandwidth(self):
    #     return self.BANDWIDTH_MAP[int(self._query('clbwth?'))]

    # @bandwidth.setter
    # def bandwidth(self, bw):
    #     assert bw in self.BANDWIDTH_MAP.values()
    #     target = reversed_dict(self.BANDWIDTH_MAP)[bw]
    #     self._query('clbwth %d' % target)




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


