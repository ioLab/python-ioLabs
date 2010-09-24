# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
from ioLabs import USBBox

usbbox=USBBox()

usbbox.serial.write('testing hello world')

while True:
    bytes=usbbox.serial.read()
    if bytes:
        print bytes