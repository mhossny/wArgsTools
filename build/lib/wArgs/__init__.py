'''wArgsTools
Author: Mo Hossny
Email: m.hossny@research.deakin.edu.au

This module encapsulates functions and classes to parse args and kwargs of
callable object and construct `argparse` argument parser. The callable
arguments are then inferred from the command line arguments via `sys.argv`.
In general `*args` are added as required and `**kwargs` are added with their
corresponding defaults. argument types are inferred from `kwargs` default
values. The module relies heavily on `argparse` and `inspect` modules.

Exported Functionalities
- wArgsCall: Eager argument parsing for any callable (e.g. function, class instantiation, lambda's)
- wArgs: Lazy argument parsing of callabels which returns a callable object to call later. Does not support class inheritance.
- wArgsClass: Lazy argument parsing of classes which returns a class_wArgs to instantiate objects from it later. Supports inheritance
- wArgsInit: Allows entry point to globals into thee wArgs.core module. Essential for python eval'd arguments (e.g. None and object)
- wArgsCheck: Checks for -h/--help and unrecognised arguments.
- wArgsHelp: Produces help of all objects using wArgs. 
- wildArgs: Lite weight and EAGER wArgs encapsulator allows on the spot CLI arg for a selected local variables.

## TODO:
24/04/20 - Clean wArgsCheck and use Levenshtein Distance and argmax for prefixed arg matching
22/04/20 - Add chooices support (e.g. set?)
22/04/20 - Add CLI dictionary support (e.g. --dictarg k1:v1 k2:v2 ...)
22/04/20 - Add Ellipsis support (e.g. f(x=...) -> ???)
22/04/20 - Allow importing modules for python eval'd args (e.g. --import math, --import_from math pi log sin)

04/01/20 - Fix mutability of unknown_args
10/01/20 - Add custom help formatter

## DONE:
24/06/20 - Fixed a bug with prefixed args reportede as unknown args (Needs more work. Chk TODOs)
22/04/20 - Fixed EvalArgParseAction cannot access membeers of loaded modules (e.g. nn.MSE)
21/04/20 - Fixed boolean args defalted to True. Now defaults to False and a `no` prefix is added to arg name (e.g. Flag -> --noFl\
ag)
21/04/20 - Add docstring support
20/04/20 - Supports inheritance
20/04/20 - fixed inheritance order (reversed(callableobj.mro()))
20/04/20 - fixed force_pos_args in wArgsClass
'''
import sys

__VERSION__ = '0.1.0'
print(f'wArgsTools v{__VERSION__} is still under development!!!!\n\n', file=sys.stderr)

from .core import EvalArgParseAction

from .tools import make_wArgs as wArgs
from .tools import hlp_wArgs as wArgsHelp
from .tools import chk_wArgs as wArgsCheck
from .tools import call_wArgs as wArgsCall
from .tools import makeC_wArgs_Ex as wArgsClass
from .tools import struct, localparams
from .tools import wildArgs as wildArgs, mkWildArgs

#wArgsHlp = wArgsHelp
wArgsChk = wArgsCheck
#wArgsCls = wArgsClass
#wArgsFun = wArgsCall

from argparse import ArgumentError
from . import core

wArgsInit = core.update_globals
