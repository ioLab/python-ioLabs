'''
The OS X HID interface module.
Dynamically loaded on OS X.
Refer to the hid module for available functions
'''

from ctypes import *
from ctypes.util import find_library

import logging
import struct

# common code for OS X and win32
from hid import HIDDevice
from hid.cparser import define, parse

# define various types we'll be using (so we can match name from headers)

define('mach_port_t',  'void*')
define('io_object_t',  'void*')
define('io_iterator_t','void*')
define('io_service_t', 'void*')
define('LPVOID', 'void*')
define('Boolean',c_ubyte)
define('UInt16',c_uint16)
define('SInt32',c_int32)
define('UInt32',c_uint32)
define('uint32_t',c_uint32)
define('UInt64',c_uint64)
define('ULONG',c_ulong)
define('IOReturn',c_int)
define('CFRunLoopSourceRef', 'void*')
define('CFDictionaryRef', 'void*')
define('CFArrayRef', 'void*')
define('AbsoluteTime', 'UInt64')
define('CFTimeInterval', 'double')
define('__CFString', 'void*') # opaque datatype
define('CFStringRef', '__CFString*')
define('__CFAllocator', 'void*')
define('CFAllocatorRef', '__CFAllocator*')
define('CFStringEncoding', 'UInt32')
define('__CFNumber', 'void*')
define('CFNumberRef', '__CFNumber*')
define('CFNumberType',c_int) # enum

# 128 bit identifier
class CFUUIDBytes(Structure):
    _fields_ = [ ('bytes0_15', c_ubyte * 16) ]

define('CFUUIDBytes',CFUUIDBytes)
define('REFIID','CFUUIDBytes')

define('IOHIDElementCookie','void*')
define('IOHIDElementType',c_int) # enum 

define('IOHIDQueueInterface','void*')
define('IOHIDOutputTransactionInterface','void*')
define('IOHIDReportType',c_int) # enum

define('HRESULT','SInt32')

IOHIDCallbackFunction=parse('void (*IOHIDCallbackFunction)(void *target, IOReturn result, void *refcon, void *sender)').ctype
define('IOHIDCallbackFunction',IOHIDCallbackFunction)

IOHIDElementCallbackFunction=parse('void (*IOHIDElementCallbackFunction)(void *target, IOReturn result, void *refcon, void *sender, IOHIDElementCookie elementCookie)').ctype
define('IOHIDElementCallbackFunction',IOHIDElementCallbackFunction)

IOHIDReportCallbackFunction=parse('void ( *IOHIDReportCallbackFunction) ( void *target, IOReturn result, void *refcon, void *sender, uint32_t bufferSize)').ctype
define('IOHIDReportCallbackFunction',IOHIDReportCallbackFunction)

class IOHIDEventStruct(Structure):
    _fields_=[
        parse('IOHIDElementType type').cstruct,
        parse('IOHIDElementCookie elementCookie').cstruct,
        parse('SInt32 value').cstruct,
        parse('AbsoluteTime timestamp').cstruct,
        parse('UInt32 longValueSize').cstruct,
        parse('void * longValue').cstruct,
    ]

define('IOHIDEventStruct',IOHIDEventStruct)

mach_port_t=c_void_p

io_object_t=mach_port_t
io_iterator_t=io_object_t

SInt32=c_int
UInt32=c_uint
UInt64=c_ulonglong
IOReturn=c_int
CFRunLoopSourceRef=c_void_p
CFDictionaryRef=c_void_p
CFArrayRef=c_void_p
AbsoluteTime=UInt64
CFTimeInterval=c_double

REFIID=CFUUIDBytes


IOHIDElementCookie=c_void_p
IOHIDElementType=c_int # enum 

IOHIDQueueInterface=c_void_p
IOHIDOutputTransactionInterface=c_void_p

IOHIDReportType=c_int # enum
# enum values for IOHIDReportType
kIOHIDReportTypeInput=0
kIOHIDReportTypeOutput=1
kIOHIDReportTypeFeature=2
kIOHIDReportTypeCount=3
#



########################################################
# COM interface structures
IUNKNOWN_C_GUTS=[
    parse('void *_reserved').cstruct,
    parse('HRESULT (*QueryInterface)(void *thisPointer, REFIID iid, LPVOID *ppv)').cstruct,
    parse('ULONG (*AddRef)(void *thisPointer)').cstruct,
    parse('ULONG (*Release)(void *thisPointer)').cstruct,
]

IOCFPLUGINBASE=[
    parse('UInt16 version').cstruct,
    parse('UInt16 revision').cstruct,
    parse('IOReturn (*Probe)(void *thisPointer, CFDictionaryRef propertyTable,'
                    'io_service_t service, SInt32 * order)').cstruct,
    parse('IOReturn (*Start)(void *thisPointer, CFDictionaryRef propertyTable,'
                     'io_service_t service)').cstruct,
    parse('IOReturn (*Stop)(void *thisPointer)').cstruct,
]


IOHIDDEVICEINTERFACE_FUNCS_100=[
    parse('IOReturn (*createAsyncEventSource)(void * self, CFRunLoopSourceRef * source)').cstruct,
    parse('CFRunLoopSourceRef (*getAsyncEventSource)(void * self)').cstruct,
    parse('IOReturn (*createAsyncPort)(void * self, mach_port_t * port)').cstruct,
    parse('mach_port_t (*getAsyncPort)(void * self)').cstruct,
    parse('IOReturn (*open)(void * self, UInt32 flags)').cstruct,
    parse('IOReturn (*close)(void * self)').cstruct,
    parse('IOReturn (*setRemovalCallback)(void * self, IOHIDCallbackFunction removalCallback,'
                                   'void * removalTarget, void * removalRefcon)').cstruct,
    parse('IOReturn (*getElementValue)(void * self, IOHIDElementCookie	elementCookie,'
                                'IOHIDEventStruct * valueEvent)').cstruct,
    parse('IOReturn (*setElementValue)(void * self, IOHIDElementCookie elementCookie,'
                                'IOHIDEventStruct * valueEvent, UInt32 timeoutMS,'
                                'IOHIDElementCallbackFunction callback,'
                                'void * callbackTarget, void * callbackRefcon)').cstruct,
    parse('IOReturn (*queryElementValue)(void * self, IOHIDElementCookie elementCookie,'
                                'IOHIDEventStruct * valueEvent, UInt32 timeoutMS,'
                                'IOHIDElementCallbackFunction callback,'
                                'void * callbackTarget, void * callbackRefcon)').cstruct,
    parse('IOReturn (*startAllQueues)(void * self)').cstruct,
    parse('IOReturn (*stopAllQueues)(void * self)').cstruct,
    parse('IOHIDQueueInterface ** (*allocQueue) (void *self)').cstruct,
    parse('IOHIDOutputTransactionInterface ** (*allocOutputTransaction) (void *self)').cstruct,
]

IOHIDDEVICEINTERFACE_FUNCS_121=[
    parse('IOReturn (*setReport)(void * self, IOHIDReportType reportType, UInt32 reportID,'
                                    'void * reportBuffer, UInt32 reportBufferSize,'
                                    'UInt32 timeoutMS, IOHIDReportCallbackFunction callback,'
                                    'void * callbackTarget, void * callbackRefcon)').cstruct,
    parse('IOReturn (*getReport)(void * self, IOHIDReportType reportType,'
                                    'UInt32 reportID, void * reportBuffer,'
                                    'UInt32 * reportBufferSize, UInt32 timeoutMS,'
                                    'IOHIDReportCallbackFunction callback,'
                                    'void * callbackTarget, void * callbackRefcon)').cstruct,
]

IOHIDDEVICEINTERFACE_FUNCS_122=[
    parse('IOReturn (*copyMatchingElements)(void * self, CFDictionaryRef matchingDict,'
                                    'CFArrayRef * elements)').cstruct,
    parse('IOReturn (*setInterruptReportHandlerCallback)(void * self, void * reportBuffer,'
                                    'UInt32 reportBufferSize,'
                                    'IOHIDReportCallbackFunction callback,'
                                    'void * callbackTarget, void * callbackRefcon)').cstruct,
]

class IOCFPlugInInterfaceStruct(Structure):
    _fields_= IUNKNOWN_C_GUTS \
            + IOCFPLUGINBASE

class IOHIDDeviceInterface122(Structure):
    _fields_= IUNKNOWN_C_GUTS \
            + IOHIDDEVICEINTERFACE_FUNCS_100 \
            + IOHIDDEVICEINTERFACE_FUNCS_121 \
            + IOHIDDEVICEINTERFACE_FUNCS_122

########################################################

########################################################
# class to handle COM object references
class COMObjectRef:
    def __init__(self,ref):
        self.ref=ref
        logging.info("created: %s",self)
    
    def __del__(self):
        logging.info("releasing: %s",self)
        self.Release()
    
    def __nonzero__(self):
        return self.ref is not None
    
    def __str__(self):
        return 'COMObjectRef(%s)' % self.ref
    
    def __getattr__(self,name):
        '''
        return a function on the com object
        (takes care of passing in the ref as the first arg)
        '''
        fn=getattr(self.ref.contents.contents,name)
        return lambda *arg: fn(self.ref,*arg)

########################################################

KERN_SUCCESS=0

kIOReturnSuccess=0
kIOHIDDeviceKey="IOHIDDevice"
kIOHIDVendorIDKey="VendorID"
kIOHIDProductIDKey="ProductID"

kIOMasterPortDefault=None

kCFAllocatorDefault=None
kCFStringEncodingASCII = 0x0600
kCFNumberIntType=9
kNilOptions=''

# load the CoreFoundation Library
cfLibraryLocation=find_library('CoreFoundation')
logging.info('loading CoreFoundation from: %s',cfLibraryLocation)
cf=CDLL(cfLibraryLocation)

# CoreFoundation Functions we'll be using
CFDictionaryGetValue=parse('void *CFDictionaryGetValue(CFDictionaryRef theDict, void *key)').from_lib(cf)
CFStringCreateWithCString=parse('CFStringRef CFStringCreateWithCString(CFAllocatorRef alloc, char *cStr, CFStringEncoding encoding)').from_lib(cf)
CFNumberGetValue=parse('Boolean CFNumberGetValue(CFNumberRef number, CFNumberType theType, void *valuePtr)').from_lib(cf)
CFRelease=cf.CFRelease
CFUUIDGetConstantUUIDWithBytes=cf.CFUUIDGetConstantUUIDWithBytes
CFUUIDGetUUIDBytes=cf.CFUUIDGetUUIDBytes
CFUUIDGetUUIDBytes.restype=CFUUIDBytes
CFRunLoopAddSource=cf.CFRunLoopAddSource
CFRunLoopGetCurrent=cf.CFRunLoopGetCurrent
CFRunLoopRunInMode=cf.CFRunLoopRunInMode
CFRunLoopRunInMode.argtypes = [ c_void_p, CFTimeInterval, c_int ]

# CFSTR was a macro so we'll use a function instead
def CFSTR(cstr):
    return CFStringCreateWithCString(kCFAllocatorDefault,cstr,kCFStringEncodingASCII)

# CoreFoundation constant
kCFRunLoopDefaultMode=c_void_p.in_dll(cf,"kCFRunLoopDefaultMode")

# Load IOKit
iokitLibraryLocation=find_library('IOKit')
logging.info('loading IOKit from: %s',iokitLibraryLocation)
iokit=CDLL(iokitLibraryLocation)

# IOKit functions we'll be using
IOIteratorNext=iokit.IOIteratorNext
IOIteratorNext.restype=io_object_t
IOObjectRelease=iokit.IOObjectRelease
IOServiceMatching=iokit.IOServiceMatching
IOServiceGetMatchingServices=iokit.IOServiceGetMatchingServices
IOCreatePlugInInterfaceForService=iokit.IOCreatePlugInInterfaceForService

# constants
kIOHIDDeviceUserClientTypeID = CFUUIDGetConstantUUIDWithBytes(None,
    0xFA, 0x12, 0xFA, 0x38, 0x6F, 0x1A, 0x11, 0xD4,
    0xBA, 0x0C, 0x00, 0x05, 0x02, 0x8F, 0x18, 0xD5)

kIOCFPlugInInterfaceID = CFUUIDGetConstantUUIDWithBytes(None,
    0xC2, 0x44, 0xE8, 0x58, 0x10, 0x9C, 0x11, 0xD4,
    0x91, 0xD4, 0x00, 0x50, 0xE4, 0xC6, 0x42, 0x6F)

kIOHIDDeviceInterfaceID = CFUUIDGetConstantUUIDWithBytes(None,
    0x78, 0xBD, 0x42, 0x0C, 0x6F, 0x14, 0x11, 0xD4,
    0x94, 0x74, 0x00, 0x05, 0x02, 0x8F, 0x18, 0xD5)

def find_hid_devices():
    '''
    query the host computer for all available HID devices
    and returns a list of any found
    '''
    devices=[]
    
    hidMatchDictionary = IOServiceMatching(kIOHIDDeviceKey);
    
    hidObjectIterator=io_iterator_t()
    
    result=IOServiceGetMatchingServices(kIOMasterPortDefault,hidMatchDictionary,byref(hidObjectIterator))
    if result != kIOReturnSuccess or not hidObjectIterator:
        raise RuntimeError("Can't obtain an IO iterator")

    try:
        while True:
            hidDevice = IOIteratorNext(hidObjectIterator)
            if not hidDevice:
                break
            
            dev=OSXHIDDevice(hidDevice,0,0)
            
            hidProperties=c_void_p()
            result = iokit.IORegistryEntryCreateCFProperties(hidDevice,byref(hidProperties),kCFAllocatorDefault,kNilOptions)
            if result == KERN_SUCCESS and hidProperties:
                vendor,product=0,0
                vendorRef = CFDictionaryGetValue(hidProperties, CFSTR(kIOHIDVendorIDKey));
                productRef = CFDictionaryGetValue(hidProperties, CFSTR(kIOHIDProductIDKey));
                
                if vendorRef:
                    vendor=c_int()
                    CFNumberGetValue(parse('CFNumberRef').cast(vendorRef),kCFNumberIntType,byref(vendor))
                    CFRelease(vendorRef)
                    vendor=vendor.value
                
                if productRef:
                    product=c_int()
                    CFNumberGetValue(parse('CFNumberRef').cast(productRef),kCFNumberIntType,byref(product))
                    CFRelease(productRef)
                    product=product.value
                
                dev.vendor=vendor
                dev.product=product
            
            logging.info("find_hid_devices: found device vendor=0x%04x product=0x%04x",dev.vendor,dev.product)
            devices.append(dev)
    finally:
        IOObjectRelease(hidObjectIterator)
    return devices

class OSXHIDDevice(HIDDevice):
    '''
    class representing a HID device on the host (OS X) computer
    '''
    def __init__(self,hidDevice,vendor,product):
        '''
        create the hid device wrapper
        hidDevice is a handle from the OS
        '''
        HIDDevice.__init__(self,vendor,product)
        self.IOObjectRelease=IOObjectRelease # need to hold onto reference to release function
        self._hidDevice=hidDevice
        self._hidInterface=None
    
    def __del__(self):
        HIDDevice.__del__(self)
        if self._hidDevice:
            logging.info("releasing HID device: %s"%self)
            self.IOObjectRelease(self._hidDevice)
    
    def close(self):
        # should be sufficient to get callback thread to quit
        if self._hidInterface:
            self._hidInterface=None
        HIDDevice.close(self)
    
    def is_open(self):
        '''
        see if the device is open
        '''
        return self._hidInterface is not None
    
    def open(self):
        '''
        open the HID device - must be called prior to registering callbacks
        or setting reports
        '''
        if not self.is_open():
            logging.info("opening hid device")
            # plugInInterface initialised to NULL
            plugInInterface=COMObjectRef(POINTER(POINTER(IOCFPlugInInterfaceStruct))())
            score=UInt32()
            IOCreatePlugInInterfaceForService(self._hidDevice, kIOHIDDeviceUserClientTypeID,
            	kIOCFPlugInInterfaceID, byref(plugInInterface.ref), byref(score));
            
            
            # query to get the HID interface
            hidInterface=POINTER(POINTER(IOHIDDeviceInterface122))()
            plugInInterface.QueryInterface(CFUUIDGetUUIDBytes(kIOHIDDeviceInterfaceID),parse('LPVOID*').cast(byref(hidInterface)))
            
            self._hidInterface=COMObjectRef(hidInterface)
            
            # open the HID device
            self._hidInterface.open(0)
        else:
            loggging.info("device already open")
    
    def set_report(self,report_data,report_id=0):
        '''
        "set" a report - send the data to the device (which must have been opened previously)
        '''
        HIDDevice.set_report(self,report_data,report_id)
        
        # copy data into a ctypes buffer
        report_buffer=(c_ubyte*len(report_data))()
        for i,c in enumerate(report_data):
            report_buffer[i]=struct.unpack('B',c)[0]
        
        self._hidInterface.setReport(
            kIOHIDReportTypeOutput,
            report_id,
            report_buffer,
            len(report_buffer),
            100, # 100ms
            IOHIDReportCallbackFunction(), None, None # NULL callback
        )
    
    def _run_interrupt_callback_loop(self,report_buffer_size):
        '''
        run on a thread to handle reading events from the device
        '''
        if not self.is_open():
            raise RuntimeError("device not open")
        
        logging.info("starting _run_interrupt_callback_loop")
        
        # create the report buffer
        report_buffer=(c_ubyte*report_buffer_size)() # TODO should query device to find report size
        
        # create the callback function that actually calls the user defined callback
        def callback(target, result, refcon, sender, size):
            # copy data out of report buffer
            if self._callback is not None:
                report_data="".join([struct.pack('B',b) for b in report_buffer])
                # zero buffer after to ensure we don't get weird-ness
                # if it's not fully written to later
                for i in range(len(report_buffer)):
                    report_buffer[i]=0
                logging.info('interrupt_report_callback(%r)',report_data)
                self._callback(self,report_data)
        
        # make sure we hold into the callback, so it doesn't get gc-ed
        # (leads to weird behaviour)
        hid_callback=IOHIDReportCallbackFunction(callback)
        
        port=mach_port_t()
        self._hidInterface.createAsyncPort(byref(port))
        eventSource=CFRunLoopSourceRef()
        self._hidInterface.createAsyncEventSource(byref(eventSource))
        
        # set the C callback
        self._hidInterface.setInterruptReportHandlerCallback(
            byref(report_buffer),
            len(report_buffer),
            hid_callback,
            None,None)
        
        # kick off the queues etc
        self._hidInterface.startAllQueues()
        CFRunLoopAddSource(CFRunLoopGetCurrent(), eventSource, kCFRunLoopDefaultMode)
        
        logging.info("running CFRunLoopRunInMode")
        
        while self._running and self.is_open():
            CFRunLoopRunInMode(kCFRunLoopDefaultMode,0.1,False)
    
__all__ = ['find_hid_devices','OSXHIDDevice']