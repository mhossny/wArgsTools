#!/Users/mo/anaconda3/bin/python
import sys
import pdb
import pytest
from .. import wArgs, wArgsCall, wArgsHelp, wArgsChk, wArgsClass, wArgsInit, ArgumentError


def f1(test_int=1, test_str='abc', test_float=2.2, test_none=None):
    return '\n'.join([f'{k} -> {v}' for k, v in locals().items()])

def test_default_kwargs_passes():
    argvtxt = __file__.split('/')[-1]

    sys.argv = argvtxt.split()

    correct_formatted_args = f1()
    test_formatted_args = wArgsCall(f1)
    
    assert correct_formatted_args == test_formatted_args
    
def test_kwargs_passes():
    argvtxt = __file__.split('/')[-1]
    test_int, test_str, test_float, test_none = 10, 'myname', 3.14, 22.0/7.0
    argvtxt += f' --test_int={test_int} --test_float={test_float}'
    argvtxt += f' --test_str={test_str} --test_none={test_none}'

    sys.argv = argvtxt.split()

    test_vars = {k: v for k, v in locals().items() if k.startswith('test_')}
    correct_formatted_args = f1(**test_vars)
    test_formatted_args = wArgsCall(f1)
    
    assert correct_formatted_args == test_formatted_args



    
def f2(flag1=False, flag2=False, flag3=False):
    return '\n'.join([f'{k} -> {v}' for k, v in locals().items()])

def test_default_bool_kwargs_passes():
    argvtxt = __file__.split('/')[-1]

    sys.argv = argvtxt.split()

    correct_formatted_args = f2()
    test_formatted_args = wArgsCall(f2)
    
    assert correct_formatted_args == test_formatted_args
    
def test_bool_kwargs_passes():
    argvtxt = __file__.split('/')[-1]
    argvtxt += f' --flag1 --flag2 1 --flag3 1'

    sys.argv = argvtxt.split()

    correct_formatted_args = f2(flag1=True, flag2=True, flag3=True)
    test_formatted_args = wArgsCall(f2)
    
    assert correct_formatted_args == test_formatted_args
    
def test_bool_kwargs_equalsexits():
    argvtxt = __file__.split('/')[-1]
    argvtxt += f' --flag1 --flag2=1 --flag3 1'

    sys.argv = argvtxt.split()

    correct_formatted_args = f2(flag1=True, flag2=True, flag3=True)
    with pytest.raises(SystemExit):
        test_formatted_args = wArgsCall(f2)
        assert correct_formatted_args == test_formatted_args
    



def f3(test_int, test_str, test_float=2.2, test_none=None):
    return '\n'.join([f'{k} -> {v}' for k, v in locals().items()])


def test_argv_passed_required_args_passes():
    argvtxt = __file__.split('/')[-1]
    test_int, test_str, test_float, test_none = 10, 'myname', 3.14, 22.0/7.0
    argvtxt += f' --test_int={test_int} --test_float={test_float}'
    argvtxt += f' --test_str={test_str} --test_none={test_none}'

    sys.argv = argvtxt.split()

    test_vars = {k: v for k, v in locals().items() if k.startswith('test_')}
    correct_formatted_args = f3(**test_vars)
    test_formatted_args = wArgsCall(f3, parse_pos_args=True)
    
    assert correct_formatted_args == test_formatted_args

def test_missing_required_args_fails():
    argvtxt = __file__.split('/')[-1]
    test_float, test_none = 3.14, 22.0/7.0
    argvtxt += f' --test_float={test_float}'
    argvtxt += f' --test_none={test_none}'

    sys.argv = argvtxt.split()

    test_vars = {k: v for k, v in locals().items() if k.startswith('test_')}
    correct_formatted_args = f3(1, 2, **test_vars)

    with pytest.raises(TypeError):    
        test_formatted_args = wArgsCall(f3)
        assert correct_formatted_args == test_formatted_args

def test_locally_passed_required_args_passes():
    argvtxt = __file__.split('/')[-1]
    test_float, test_none = 3.14, 22.0/7.0
    argvtxt += f' --test_float={test_float}'
    argvtxt += f' --test_none={test_none}'

    sys.argv = argvtxt.split()

    test_vars = {k: v for k, v in locals().items() if k.startswith('test_')}
    correct_formatted_args = f3(1, 2, **test_vars)
    test_formatted_args = wArgsCall(f3, 1, 2)
    
    assert correct_formatted_args == test_formatted_args


