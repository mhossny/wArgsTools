# wArgsTools Package Version 0.2 

This is a simple package which inspects callables and constructs an argparse.
Most permissive thing ever. Use it anyway you want for any purpose you want.

This module encapsulates functions and classes to parse args and kwargs of
callable object and construct `argparse` argument parser. The callable
arguments are then inferred from the command line arguments via `sys.argv`.
In general `*args` are added as required and `**kwargs` are added with their
corresponding defaults. argument types are inferred from `kwargs` default
values. The module relies heavily on `argparse` and `inspect` modules.

## Exported Functionalities
- wArgsCall: Eager argument parsing for any callable (e.g. function, class instantiation, lambda's)
- wArgs: Lazy argument parsing of callabels which returns a callable object to call later. Does not support class inheritance.
- wArgsClass: Lazy argument parsing of classes which returns a class_wArgs to instantiate objects from it later. Supports inherit\
ance
- wArgsInit: Allows entry point to globals into the wArgs.core module. Essential for python eval'd arguments (e.g. None and obje\
ct)
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

Author: Mo Hossny
Email: m.hossny@research.deakin.edu.au

## LICENSE
Most permissive thing ever. Use it anyway you want for any purpose you want.

MIT License

Copyright (c) 2019 Mo Hossny

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.