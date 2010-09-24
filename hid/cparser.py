# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
from ctypes import *
import re

TOKENS=re.compile(r'[\w_]+|[()*,]')
WORD=re.compile(r'^[_\w]+$')

_keywords=set()

_types={}

def define(name, t):
    if isinstance(t,basestring):
        # referencing an existing type by name
        t=_parse_type(t)
    _types[name]=t
    # assume defined types are keywords
    for token in re.findall(r'\w+', name):
        _keywords.add(token)
    return t # return the defined-type

# define standard ctypes
define('void', None)
define('void*', c_void_p)
define('char', c_char)
define('wchar_t', c_wchar)
define('unsigned char', c_ubyte)
define('short', c_short)
define('unsigned short', c_ushort)
define('int', c_int)
define('unsigned int', c_uint)
define('long', c_long)
define('unsigned long', c_ulong)
define('long long', c_longlong)
define('unsigned long long', c_ulonglong)
define('float', c_float)
define('double', c_double)
define('char*', c_char_p)
define('wchar_t*', c_wchar_p)


def _parse_type(type_str):
    # see if the type is there
    if _types.has_key(type_str):
        return _types[type_str]
    if type_str.endswith('*'):
        type_str=type_str[:-1]
        return POINTER(_parse_type(type_str))
    else:
        raise ValueError("unknown type: " + type_str)

class tokenizer(object):
    def __init__(self,s):
        self.s=s
        # parse raw tokens, then group adjacent keywords
        # together to treat them like one token (e.g. 'unsigned int')
        tokens=TOKENS.findall(s)
        self.tokens=[]
        k=[]
        for t in tokens:
            if t in _keywords:
                k.append(t)
            else:
                if len(k) > 0:
                    self.tokens.append(' '.join(k))
                    k=[]
                self.tokens.append(t)
        if len(k) > 0:
            self.tokens.append(' '.join(k))
        
        self.i=-1
    
    def next(self):
        if self.empty():
            raise ValueError('no more tokens found parsing - %s' % self.s)
        self.i+=1
        return self.current()
    
    def current(self):
        return self.tokens[self.i]
    
    def push_back(self):
        if self.i < 0:
            raise ValueError('pushed back too far parsing - %s' % self.s)
        self.i-=1
    
    def empty(self):
        # are we at the last element
        return self.i >= (len(self.tokens)-1)



class c_type(object):
    def __init__(self,type_name,name=''):
        self.type_name=type_name
        self.name=name
    
    @property
    def ctype(self):
        return _parse_type(self.type_name)            
    
    @property
    def cstruct(self):
        '''convert the type for use in a struct'''
        return (self.name, self.ctype)
    
    def cast(self,value):
        return cast(value,self.ctype)
    
    def __repr__(self):
        if self.name:
            return u'c_type(%s %s)' % (self.type_str, self.name)
        return u'c_type(%s)' % self.type_str

class c_function(object):
    def __init__(self,return_type, name, param_list):
        self.return_type=return_type
        self.name=name
        self.param_list=param_list
    
    @property
    def ctype(self):
        params=[p.ctype for p in self.param_list]
        return CFUNCTYPE(self.return_type.ctype, *params)
    
    @property
    def cstruct(self):
        '''convert the type for use in a struct'''
        return (self.name, self.ctype)
    
    def from_lib(self,lib):
        fn=getattr(lib,self.name)
        fn.restype=self.return_type.ctype
        fn.argtypes=[p.ctype for p in self.param_list]
        return fn
    
    def __repr__(self):
        return u'c_function(%s %s %s)' % (self.return_type, self.name, self.param_list)

def parse_type(t):
    # grab variable name (including * for pointers)
    base_type=t.next()
    while not t.empty():
        if t.next() == '*':
            base_type += '*'
        else:
            t.push_back()
            break
    return c_type(base_type)

def parse_fn_name(t):
    if t.next() == '(':
        # fn pointer name
        assert t.next() == '*'
        name=t.next()
        assert t.next() == ')'
    else:
        name=t.current()
    return name

def parse_param(t):
    param_type=parse_type(t)
    name=t.next()
    if WORD.match(name):
        param_type.name=name
    else:
        # un-named param
        t.push_back()
    return param_type
        

def parse_param_list(t):
    assert t.next() == '('
    params=[]
    while t.next() != ')':
        t.push_back()
        params.append(parse_param(t))
        if t.next() != ',':
            break
    assert t.current() == ')'
    return params



def parse(s):
    '''
    parse a c definition/declaration returning a variable def, function def etc
    as appropriate
    '''
    t=tokenizer(s)
    def_type = parse_type(t)
    if not t.empty():
        if t.next() == '(':
            # looks like we're parsing a function pointer definition
            # e.g. void (*my_fn)(void)
            t.push_back()
            fn_name = parse_fn_name(t)
            param_list = parse_param_list(t)
            if not t.empty():
                raise ValueError("unexpected tokens at end of function def in - %s" % s)
            return c_function(def_type, fn_name, param_list)
        else:
            t.push_back()
            name = t.next()
            if not t.empty():
                if t.next() == '(':
                    # parsing function def again (regular def not pointer)
                    # e.g. void my_fn(void)
                    t.push_back()
                    param_list = parse_param_list(t)
                    if not t.empty():
                        raise ValueError("unexpected tokens at end of function def in - %s" % s)
                    return c_function(def_type, name, param_list)
                else:
                    pass
                    # might be parsing array definition
            if not t.empty():
                raise ValueError("unexpected tokens at end of variable def in - %s" % s)
            # named variable declaration
            def_type.name=name
            return def_type
    else:
        # un-named variable type declatation
        return def_type


__all__ = ['parse', 'define']