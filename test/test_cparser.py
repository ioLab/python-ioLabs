# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
from hid.cparser import *
from hid.cparser import tokenizer

import ctypes

def test_tokenizer():
    t=tokenizer('void* my_fn(void)')
    assert not t.empty()
    assert t.next() == 'void'
    assert t.next() == '*'
    assert t.next() == 'my_fn'
    assert t.next() == '('
    assert t.next() == 'void'
    assert t.next() == ')'
    assert t.empty()

def test_tokenizer_keywords():
    define('long long', ctypes.c_longlong)
    t=tokenizer('void* my_fn(long long)')
    assert not t.empty()
    assert t.next() == 'void'
    assert t.next() == '*'
    assert t.next() == 'my_fn'
    assert t.next() == '('
    assert t.next() == 'long long'
    assert t.next() == ')'
    assert t.empty()


def test_parse_fn_ptr():
    fn=parse('CFRunLoopSourceRef (*GetInterfaceAsyncEventSource)(void *self)')
    assert fn.name == 'GetInterfaceAsyncEventSource'
    
    return_type=fn.return_type
    assert return_type.name == ''
    assert return_type.type_name == 'CFRunLoopSourceRef'
    
    param_list = fn.param_list
    assert len(param_list) == 1
    
    param=param_list[0]
    assert param.name == 'self'
    assert param.type_name == 'void*'

def test_parse_fn():
    fn=parse('CFRunLoopSourceRef GetInterfaceAsyncEventSource(void *self)')
    assert fn.name == 'GetInterfaceAsyncEventSource'
    
    return_type=fn.return_type
    assert return_type.name == ''
    assert return_type.type_name == 'CFRunLoopSourceRef'
    
    param_list = fn.param_list
    assert len(param_list) == 1
    
    param=param_list[0]
    assert param.name == 'self'
    assert param.type_name == 'void*'

def test_parse_var():
    var=parse('int i')
    assert var.type_name == 'int'
    assert var.name == 'i'
    
    var=parse('int* i')
    assert var.type_name == 'int*'
    assert var.name == 'i'
    
    var=parse('int *i')
    assert var.type_name == 'int*'
    assert var.name == 'i'

def test_parse_var_type():
    var=parse('int')
    assert var.type_name == 'int'
    print var.name
    assert var.name == ''
    
    var=parse('void')
    assert var.type_name == 'void'
    assert var.name == ''
    
    var=parse('void*')
    assert var.type_name == 'void*'
    print var.name
    assert var.name == ''

def test_parse_void_ctype():
    assert parse('void').ctype is None
    assert parse('void*').ctype  == ctypes.c_void_p
    assert parse('void**').ctype == ctypes.POINTER(ctypes.c_void_p)

def test_parse_int_ctype():
    assert parse('int').ctype   == ctypes.c_int
    assert parse('int*').ctype  == ctypes.POINTER(ctypes.c_int)
    assert parse('int**').ctype == ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

def test_parse_basic_types():
    assert parse('void').ctype is None
    assert parse('void*').ctype == ctypes.c_void_p
    assert parse('char').ctype == ctypes.c_char
    assert parse('wchar_t').ctype == ctypes.c_wchar
    assert parse('unsigned char').ctype == ctypes.c_ubyte
    assert parse('short').ctype == ctypes.c_short
    assert parse('unsigned short').ctype == ctypes.c_ushort
    assert parse('int').ctype == ctypes.c_int
    assert parse('unsigned int').ctype == ctypes.c_uint
    assert parse('long').ctype == ctypes.c_long
    assert parse('unsigned long').ctype == ctypes.c_ulong
    assert parse('long long').ctype == ctypes.c_longlong
    assert parse('unsigned long long').ctype == ctypes.c_ulonglong
    assert parse('float').ctype == ctypes.c_float
    assert parse('double').ctype == ctypes.c_double
    assert parse('char*').ctype == ctypes.c_char_p
    assert parse('wchar_t*').ctype == ctypes.c_wchar_p

def test_parse_function_ctype():
    assert parse('void hello(int)').ctype       == ctypes.CFUNCTYPE(None, ctypes.c_int)
    assert parse('void hello(int name)').ctype  == ctypes.CFUNCTYPE(None, ctypes.c_int)
    assert parse('int hello(int name)').ctype   == ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
    assert parse('int hello(void *name)').ctype == ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
    assert parse('int hello(void* name)').ctype == ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)

def test_parse_function_cstruct():
    assert parse('void hello(int)').cstruct == ('hello', ctypes.CFUNCTYPE(None, ctypes.c_int))
    assert parse('int var').cstruct == ('var', ctypes.c_int)
    assert parse('void *p').cstruct == ('p', ctypes.c_void_p)
