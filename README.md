Stanford EC301 potentiostat/galvanostate device.

Implements direct control of current and potential, potential
step and cycle scans, and data acquisition. All hardware-triggered
functionality relies on the trigger signal also being connected
to the synchronous ADC input for filtering. Trigger pulses should
therefore not be shorter than the data acquisition period
(4 us - 1 ms depending on settings).

TODO:
* Error handling?

