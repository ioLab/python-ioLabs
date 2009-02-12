from hid.cparser import *

def test_tokenizer():
    t=tokenizer('void* my_fn(void)')
    assert not t.empty()
    assert t.next() == 'void'
    assert t.next() == '*'
    assert t.next() == 'my_fn'
    assert t.next() == '('
    assert t.next() == 'void'
    assert t.next() == ')'
    print t.current()
    print len(t.tokens)
    print t.i
    assert t.empty()
    

def test_parse_c_def_fn_ptr():
    fn=parse_c_def('CFRunLoopSourceRef (*GetInterfaceAsyncEventSource)(void *self)')
    assert fn.name == 'GetInterfaceAsyncEventSource'
    
    return_type=fn.return_type
    assert return_type.name == ''
    assert return_type.type_name == 'CFRunLoopSourceRef'
    
    param_list = fn.param_list
    assert len(param_list) == 1
    
    param=param_list[0]
    assert param.name == 'self'
    assert param.type_name == 'void*'

def test_parse_c_def_fn():
    fn=parse_c_def('CFRunLoopSourceRef GetInterfaceAsyncEventSource(void *self)')
    assert fn.name == 'GetInterfaceAsyncEventSource'
    
    return_type=fn.return_type
    assert return_type.name == ''
    assert return_type.type_name == 'CFRunLoopSourceRef'
    
    param_list = fn.param_list
    assert len(param_list) == 1
    
    param=param_list[0]
    assert param.name == 'self'
    assert param.type_name == 'void*'

def test_parse_c_def_var():
    var=parse_c_def('int i')
    assert var.type_name == 'int'
    assert var.name == 'i'
    
    var=parse_c_def('int* i')
    assert var.type_name == 'int*'
    assert var.name == 'i'
    
    var=parse_c_def('int *i')
    assert var.type_name == 'int*'
    assert var.name == 'i'

def test_parse_c_def_var_type():
    var=parse_c_def('int')
    assert var.type_name == 'int'
    print var.name
    assert var.name == ''
    
    var=parse_c_def('void')
    assert var.type_name == 'void'
    assert var.name == ''
    
    var=parse_c_def('void*')
    assert var.type_name == 'void*'
    print var.name
    assert var.name == ''