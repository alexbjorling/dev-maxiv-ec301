import ec301lib

# Tango imports
# from PyTango import AttrWriteType, DispLevel
# from PyTango.server import Device, DeviceMeta, attribute, command, server_run,  device_property

# define device server class here
# class regloiccDS(Device):
#     ...

def main():
    # run device server here
    # server_run((regloiccDS,))

    ec301lib.example_usage_bias()
