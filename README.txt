# Installing and Using the ioLabs Python library #

Quick answer:

* Install requirements (see below)
* Run `python setup.py install` to copy files to your `PYTHONPATH`

The library consists of:

* `ioLabs.py`
* `hid/__init__.py`
* `hid/_comming.py`
* `hid/osx.py`
* `hid/win32.py`
* `psyscopex.py`

To start using the library (once you have met the requirements listed below),
copy and `ioLabs.py`, `psyscopex.py` and the `hid` directory to somewhere on your `PYTHONPATH`.
For simplicity this can be the directory that you will be using for your project.

`ioLabs.py` is the USBBox specific code and this is what you will be using for the most part.

`hid` contains the code for the the general purpose Python HID driver and you will most likely
not need to deal with it directly - however it is used by the ioLabs module.  `hid` contains code
for OS X and Windows and will dynamically load the correct module for the OS when `hid` is imported.

`psyscopex.py` is a compatibility layer for people using PsyScopeX, as we cannot use the standard 
hid library when PsyScopeX's kernel extension is installed.

## Requirements ##

* Python 2.5+ (includes ctypes)

or

* Python 2.3.5+
* C Compiler (to compile ctypes)
* ctypes

## OS X 10.5 (Leopard) ##

Leopard ships with Python 2.5 and ctypes so no additional installation is required.

## OS X 10.4 Python 2.5 ##

1. Go to http://python.org/download/
2. Find latest version for OS X (2.5.1 at time of writing) and download .dmg
3. Open .dmg file
4. Run `MacPython.mpkg` package file
5. Enter admin password when prompted

## OS X 10.4 with Stock Python (2.3.5) ##

Need to install ctypes (requires the developer tools for a C compiler):

1. Download and install `easy_install`
 1. visit: http://peak.telecommunity.com/DevCenter/EasyInstall
 2. download: http://peak.telecommunity.com/dist/ez_setup.py
 3. run `sudo python ez_setup.py` to install
 4. if you do not have the `easy_install` command you may need to
    alter your path to include
    `/System/Library/Frameworks/Python.framework/Versions/2.3/bin`
    (where the `easy_install` script resides) or use the full path name
    when invoking e.g. 
    `/System/Library/Frameworks/Python.framework/Versions/2.3/bin/easy_install`
2. Use `easy_install` to install ctypes
 1. `sudo easy_install ctypes` (may take some time, as it has to compile everything)

## Windows XP ##

1. Go to http://python.org/download/
2. Find latest version for Windows Install Python 2.5 (2.5.1 at time of writing) and download .msi
3. Run .msi and follow installer

## Tests ##

To run unit tests for the library use `nosetests` from http://code.google.com/p/python-nose/


# USB Button Box Python API #

To get started simply import the ioLabs module and create a USBBox instance:

    from ioLabs import USBBox
    
    usbbox=USBBox()

If the physical box is not connected (or cannot be detected for some reason) an 
exception will be raised when you create this USBBox instance.

## USBBox structure ##

See the accompanying `rbox_structure` document about the high-level structure of the box.
This document specified the more object oriented API for accessing the USBBox.

## Sending Commands ##

Once you have the USBBox instance you can send commands to the USBBox.  Commands are
sent via the `commands` member variable and are named after IDs specified in the
boxes manual, only in lower case.  e.g.

    usbbox.commands.resrtc() # send RESRTC (reset realtime clock) command
    usbbox.commands.p2set(0x00) # send P2SET with value 0 (should turn on LEDs)
    usbbox.commands.dirset(1,0,0) # enable loopback mode (button presses turn on LED)

## Receiving reports ##

You can register call-back functions on the `commands` object to receive notification
about reports received from the box.  The actual reports are delivered asynchronously,
but to avoid thread safety issues they are stored on a queue until `process_received_reports`
is called.  As most events are time-stamped they can be processed as needed.

To register a call-back and have it called whenever a key is pressed one can doing something
like:

    import time
    from ioLabs import USBBox, REPORT
    # REPORT contains the report IDs
    
    usbbox=USBBox()
    def mycallback(report):
        print "got a report: %s" % report
    # register callback just for KEYDN reports
    usbbox.commands.add_callback(REPORT.KEYDN,mycallback)
    
    while True:
        usbbox.process_received_reports()
        time.sleep(0.1)

Calling `process_received_reports` in this way ensures that out call-back will be called on the
same thread as the rest of the program - avoiding any nasty surprises with asynchronous data
access.  This should also make it easier for integrating with GUI toolkits.

## Recording reports ##

Instead of registering call-backs one can instead opt to have commands sent to a file, using
the `start_recording` method on the USBBox object.  This takes a list of report IDs to record
and a file to output them to:

    import time
    from ioLabs import USBBox, REPORT

    usbbox=USBBox()
    outfile=open('output.txt')
    # record all events
    usbbox.start_recording(REPORT.ALL_IDS(),outfile)
    time.sleep(30)
    usbbox.stop_recording()
    # output.txt should now contain last 30 seconds or so events

## Miscellaneous ##

The underlying HID device for the USB Button Box is stored in `device` on the USBBox instance.
It can be accessed to manually send commands to the device using it's `set_report(report_data)`
command - simply passing a string of the bytes that should be sent in the report.


