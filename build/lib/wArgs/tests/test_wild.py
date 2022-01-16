#!/Users/mo/anaconda3/bin/python
import sys
import pdb
import pytest
from math import pi
from .. import struct, wildArgs, wArgsChk, wArgsInit

wArgsInit(globals())

def test_default_wild_kwargs_passes():
    argvtxt = __file__.split('/')[-1]

    x, y, n = 1234, 'new_name', 'pi'
    argvtxt += f' --x={x} --y {y} --n {n}'

    sys.argv = argvtxt.split()

    kwargs = struct(**dict(x=123, y='xyzabcc', z=False, n=None))
    parsed_args = wildArgs(**kwargs)
    wArgsChk()

    assert x == parsed_args.x
    assert y == parsed_args.y
    assert eval(n) == parsed_args.n
    
    

