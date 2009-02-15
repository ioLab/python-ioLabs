'''
module for handling USB boxes connected via psyscopex install, which circumcents the
usual HID driver.

we provide a HID "emulation" layer, so the rest of the code interacts with this in
the same way as for a HID device
'''

import logging

from hid import HIDDevice

try:
    from hid.osx import IOObjectRelease, find_usb_devices
    on_osx=True
except:
    on_osx=False

kIOUSBDeviceClassName="IOUSBDevice"
kUSBVendorID="idVendor"
kUSBProductID="idProduct"

def find_devices():
    # attempt to directly find usb devices via
    # this function from hid lib (fail gracefully if
    # we're not running on os x)
    if on_osx:
        return find_usb_devices(kIOUSBDeviceClassName,kUSBVendorID,kUSBProductID,PsyScopeXUSBDevice)
    return []

class PsyScopeXUSBDevice(HIDDevice):
    def __init__(self, dev, vendor, product):
        super(PsyScopeXUSBDevice,self).__init__(vendor,product)
        self._usbDevice=dev
        
        # cache these so they are guaranteed to be available
        # when calling __del__
        self.IOObjectRelease=IOObjectRelease
        self.logging_info=logging.info
        self._parent__del__=super(PsyScopeXUSBDevice,self).__del__
    
    def __del__(self):
        self._parent__del__()
        if self._usbDevice:
            self.logging_info("releasing USB device: %s"%self)
            self.IOObjectRelease(self._usbDevice)

if __name__ == '__main__':
    for dev in find_devices():
        print dev