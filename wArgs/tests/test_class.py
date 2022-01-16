#!/Users/mo/anaconda3/bin/python
import sys
import pdb
import pytest
from .. import wArgs, wArgsCall, wArgsHelp, wArgsChk, wArgsClass, wArgsInit, ArgumentError


class A():
    def __init__(self,
                 opt_str='string',
                 opt_int=12,
                 opt_float=1.2,
                 opt_none=None,
                 opt_itr=[],
                 opt_itrn=[1, 4]):
        self.__dict__.update(locals())
            
def test_attributes_passes():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()
    a = wArgsCall(A)
    assert hasattr(a, 'opt_str')
    assert hasattr(a, 'opt_int')
    assert hasattr(a, 'opt_float')
    assert hasattr(a, 'opt_none')
    assert hasattr(a, 'opt_itr')
    assert hasattr(a, 'opt_itrn')

def test_defaults_passes():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()
    a = wArgsCall(A)
    assert a.opt_str == 'string'
    assert a.opt_int == 12
    assert a.opt_float == 1.2
    assert a.opt_none == None
    assert a.opt_itr == []
    assert a.opt_itrn == [1, 4]
        
def test_correct_const_inputs_spaces_passes():
    argvtxt = __file__.split('/')[-1]
    opt_str, opt_int, opt_float, opt_none = 'xxx', 55, 3.9, 6.1233//2
    argvtxt += f' --opt_str {opt_str} --opt_int {opt_int} --opt_float {opt_float} --opt_none {opt_none}'

    sys.argv = argvtxt.split()
    a = wArgsCall(A)
    assert a.opt_str == opt_str
    assert a.opt_int == opt_int
    assert a.opt_float == opt_float
    assert a.opt_none == opt_none
    assert a.opt_itr == []
    assert a.opt_itrn == [1, 4]
    
def test_correct_const_inputs_equals_passes():
    argvtxt = __file__.split('/')[-1]
    opt_str, opt_int, opt_float, opt_none = 'xxx', 55, 3.9, 6.1233//2
    argvtxt += f' --opt_str={opt_str} --opt_int={opt_int} --opt_float={opt_float} --opt_none={opt_none}'

    sys.argv = argvtxt.split()

    a = wArgsCall(A)
    assert a.opt_str == opt_str
    assert a.opt_int == opt_int
    assert a.opt_float == opt_float
    assert a.opt_none == opt_none
    
def test_correct_iter_inputs_spaces_passes():
    argvtxt = __file__.split('/')[-1]
    opt_itr = 1, False, 'abc', 3.14
    argvtxt += ' --opt_itr ' + ('{} '*len(opt_itr)).format(*opt_itr)
    opt_itrn = 55, 99
    argvtxt += ' --opt_itrn ' + ('{} '*len(opt_itrn)).format(*opt_itrn)

    #pdb.set_trace()
    sys.argv = argvtxt.split()
    
    a = wArgsCall(A)
    assert a.opt_itr == [str(x) for x in opt_itr]
    assert a.opt_itrn == list(opt_itrn)
    
def test_correct_iter_inputs_equals_exits():
    argvtxt = __file__.split('/')[-1]
    opt_itr = 1, False, 'abc', 3.14
    argvtxt += ' --opt_itr=' + ('{} '*len(opt_itr)).format(*opt_itr)
    opt_itrn = 55, 99
    argvtxt += ' --opt_itrn=' + ('{} '*len(opt_itrn)).format(*opt_itrn)

    #pdb.set_trace()
    sys.argv = argvtxt.split()

    wArgs_AC = wArgs(A)
    with pytest.raises(SystemExit):
        wArgsChk()
        a = wArgs_AC()
    
def test_incorrect_iter_inputs_spaces_exits():
    argvtxt = __file__.split('/')[-1]
    opt_itr = 1, False, 'abc', 3.14
    argvtxt += ' --opt_itr ' + ('{} '*len(opt_itr)).format(*opt_itr)
    opt_itrn = 5.5, 99
    argvtxt += ' --opt_itrn ' + ('{} '*len(opt_itrn)).format(*opt_itrn)

    #pdb.set_trace()
    sys.argv = argvtxt.split()
    
    wArgs_AC = wArgs(A)
    with pytest.raises(SystemExit):
        wArgsChk()
        a = wArgs_AC()
    
def test_int_float_incorrect_const_inputs_spaces_exits():
    argvtxt = __file__.split('/')[-1]
    opt_int, opt_float = 99.0, 9
    argvtxt += f' --opt_int {opt_int} --opt_float {opt_float}'

    sys.argv = argvtxt.split()

    with pytest.raises(SystemExit):
        wArgs_AC = wArgs(A)
        wArgsChk()
        a = wArgs_AC()
    
def test_help_exits():
    argvtxt = __file__.split('/')[-1]
    argvtxt += ' --help'

    sys.argv = argvtxt.split()

    wArgs_AC = wArgs(A)
    with pytest.raises(SystemExit):
        wArgsChk()


class B(A):
    def __init__(self,
                 b_int=99,
                 b_float=9.9,
                 b_str='bbb',
                 b_none=None,
                 b_itr=[],
                 b_itrn=[3.2, 4.9, 1.1231236]):
        A.__init__(self)
        self.__dict__.update(locals())
                 
def test_inheritance_attributes_passes():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()
    a = wArgsCall(B)
    assert hasattr(a, 'opt_str')
    assert hasattr(a, 'opt_int')
    assert hasattr(a, 'opt_float')
    assert hasattr(a, 'opt_none')
    assert hasattr(a, 'opt_itr')
    assert hasattr(a, 'opt_itrn')

    assert hasattr(a, 'b_int')
    assert hasattr(a, 'b_float')
    assert hasattr(a, 'b_str')
    assert hasattr(a, 'b_itr')
    assert hasattr(a, 'b_itrn')
    
def test_inheritance_defaults_passes():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()
    a = wArgsCall(B)
    assert a.opt_str == 'string'
    assert a.opt_int == 12
    assert a.opt_float == 1.2
    assert a.opt_none == None
    assert a.opt_itr == []
    assert a.opt_itrn == [1, 4]
        
    assert a.b_int == 99
    assert a.b_float == 9.9
    assert a.b_str == 'bbb'
    assert a.b_none == None
    assert a.b_itr == []
    assert a.b_itrn == [3.2, 4.9, 1.1231236]
    
    
class C():
    def __init__(self, x, y, z):
        self.__dict__.update(locals())
        pass

def test_missing_required_args_exits():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()

    wArgsCC = wArgsClass(C, parse_pos_args=True)

    with pytest.raises(SystemExit):
        wArgsChk()
        c = wArgsCC()
        pass

def test_argv_passed_required_args_passes():
    argvtxt = __file__.split('/')[-1]
    x, y, z = 99.0, 9, 'abc'
    argvtxt += f' --x {x} --y {y} --z {z}'

    sys.argv = argvtxt.split()

    wArgsCC = wArgsClass(C, parse_pos_args=True)

    wArgsChk()
    c = wArgsCC()

    assert c.x == x
    assert c.y == y
    assert c.z == z

def test_locally_passed_required_args_passes():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()

    #pdb.set_trace()
    wArgsCC = wArgsClass(C, parse_pos_args=False)

    c = wArgsCC(1, 2, 3)
    wArgsChk()

class D(C):
    def __init__(self, a, b=2, c=4, **kwargs):
        C.__init__(self, **kwargs)
        self.__dict__.update(locals())
        

def test_inheritance_missing_required_args_exits():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()

    wArgsCC = wArgsClass(D, parse_pos_args=True)

    with pytest.raises(SystemExit):
        wArgsChk()
        c = wArgsCC()
        pass

def test_inheritance_argv_passed_required_args_passes():
    argvtxt = __file__.split('/')[-1]
    x, y, z, a = 99.0, 9, 'abc', False
    argvtxt += f' --x {x} --y {y} --z {z} --a {a}'

    sys.argv = argvtxt.split()

    wArgsCC = wArgsClass(D, parse_pos_args=True)

    wArgsChk()
    c = wArgsCC()

    assert c.x == x
    assert c.y == y
    assert c.z == z
    assert c.a == a

def test_inheritance_locally_passed_required_args_passes():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()

    #pdb.set_trace()
    wArgsCC = wArgsClass(D, parse_pos_args=False)

    c = wArgsCC(1, x=10, y=12, z=19)
    wArgsChk()

def test_inheritance_locally_passed_required_args_exits():
    argvtxt = __file__.split('/')[-1]
    sys.argv = argvtxt.split()

    #pdb.set_trace()

    
    with pytest.raises(Exception):
        wArgsCC = wArgsClass(D, parse_pos_args=False)
        wArgsChk()
        c = wArgsCC(1, 2, 3, x=10, y=12, z=19)

