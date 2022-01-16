from argparse import ArgumentParser, ArgumentError
from argparse import ArgumentDefaultsHelpFormatter
from argparse import RawTextHelpFormatter, RawDescriptionHelpFormatter

import argparse
import os
import shutil
import time
import sys
import math
import inspect
import pdb
from collections.abc import Mapping

class struct(Mapping):
    def __init__(somthing_completely_different_from_self,
                 **kwargs):
        somthing_completely_different_from_self.__dict__.update(kwargs)

    def __iadd__(somthing_completely_different_from_self, moreargs):
        somthing_completely_different_from_self.__dict__.update(moreargs.__dict__)
        return somthing_completely_different_from_self
        
    def __len__(somthing_completely_different_from_self):
        return len(vars(somthing_completely_different_from_self).keys())

    def __getitem__(somthing_completely_different_from_self, name):
        return vars(somthing_completely_different_from_self)[name]

    def keys(somthing_completely_different_from_self):
        return vars(somthing_completely_different_from_self).keys()
        
    def __iter__(somthing_completely_different_from_self):
        return iter(somthing_completely_different_from_self.keys())

    def __repr__(somthing_completely_different_from_self):
        variables = []
        for i, (k, v) in enumerate(somthing_completely_different_from_self.__dict__.items()):
            variables.append(f'{k}: {v}')
        return '\n'.join(variables)  # str(somthing_completely_different_from_self.__dict__)


localparams = lambda kw={},notin=['self']: struct(**{k:v for k, v in kw.items()
                                                  if k not in notin})

BASE_BASE_GLOBAL_PARSER = ArgumentParser(add_help=False,
                                         formatter_class=ArgumentDefaultsHelpFormatter,
                                         conflict_handler='resolve',
                                         fromfile_prefix_chars='@',
                                         allow_abbrev=False)
BASE_GLOBAL_PARSER = BASE_BASE_GLOBAL_PARSER.add_subparsers()

class EvalArgParseAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        argparse.Action.__init__(self, option_strings, dest, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        #setattr(namespace, self.dest, eval(values, globals()))
        try:
            #pdb.set_trace()
            #print(f'{values}')
            setattr(namespace, self.dest, eval(f'{values}', globals()))
        except Exception as e:
            setattr(namespace, self.dest, values)
            print(f''''(W) Failed to eval({values}). Returning \'{values}\' as string. 
            Make sure the variable exists and you callled wArgs.init(globals())''', file=sys.stderr)
            #pdb.set_trace()
            pass

update_globals = lambda d: globals().update(d)

def ___parse_args(callableobj, skipargs):
    # Parse callable signature
    argspec = inspect.getfullargspec(callableobj)
    
    if argspec.defaults is None:
        kwargs={}
    else:
        kwargs = {k: v for k, v in zip(argspec.args[-len(argspec.defaults):],
                                       argspec.defaults)}
    
    posargs = [k for k in argspec.args if k != 'self' and k not in kwargs.keys()]
    kwonlyargs = {} if argspec.kwonlydefaults is None else argspec.kwonlydefaults
    required_kwonlyargs = [k for k in argspec.kwonlyargs
                           if k not in argspec.kwonlydefaults.keys()]

    final_kwargs = {**kwargs, **kwonlyargs}
    final_required_args = [*posargs, *required_kwonlyargs]

    final_skipped_kwargs = {k: v for k, v in final_kwargs.items() if k not in skipargs}
    final_skipped_required_args = [k for k in final_required_args if k not in skipargs]

    return final_skipped_kwargs, final_skipped_required_args

def ___prep_parser(parser, final_kwargs, final_required_args, name, docstring, 
                   eval_action, parse_pos_args=False, prfx=''):
    # Populate ArgParser Arguments
    local_parser = parser.add_parser(name, add_help=False,
                                     allow_abbrev=False,
                                     description=docstring,
                                     prog=name,
                                     help='help',
                                     epilog='Examples: TODO\n\n\n',
                                     formatter_class=ArgumentDefaultsHelpFormatter)

    if parse_pos_args:
        for i, k in enumerate(final_required_args):
            local_parser.add_argument('--{}{}'.format(prfx, k), required=True, dest=k,
                                      action=EvalArgParseAction,
                                      help='REQUIRED and python eval\'ed')

    mkMetavar = lambda v: type(v).__name__.upper()
    for i, (k, v) in enumerate(final_kwargs.items()):
        if type(v) is bool and v:
            thiskey = '--{}no{}'.format(prfx, k)
        else:
            thiskey = '--{}{}'.format(prfx, k)
        if type(v) is str:
            local_parser.add_argument(thiskey, default=v,
                                      dest=k, metavar=mkMetavar(v),  # thiskey[2:],
                                      type=str, help=' ')            
        elif hasattr(v, '__iter__'):
            nargs = len(v) if len(v)>0 else '+'
            typ = type(next(iter(v))) if len(v) else str
            local_parser.add_argument(thiskey, default=v,
                                      dest=k, metavar=mkMetavar(typ()),  # thiskey[2:],
                                      type=typ, nargs=nargs, help=' ')
        elif type(v) is bool:
            local_parser.add_argument(thiskey, default=False,
                                      dest=k, #metavar=thiskey[2:],
                                      action='store_true', help=' ')
        elif v is None:
            local_parser.add_argument(thiskey, default=None,
                                      dest=k, metavar='PYTHON_CODE',  # metavar=thiskey[2:],
                                      action=eval_action,
                                      help='python eval\'ed')
        elif type(v).__name__ == 'type':  # not in dir(__builtins__):
            # print('NOT BUILTIN', type(v).__name__)
            local_parser.add_argument(thiskey, default=v,
                                      dest=k, metavar=mkMetavar(v),  # thiskey[2:],
                                      action=eval_action,
                                      type=str, help=' ')
        else:
            # print('IS BUILTIN', type(v).__name__)
            local_parser.add_argument(thiskey, default=v,
                                      dest=k, metavar=mkMetavar(v),  # thiskey[2:],
                                      type=type(v), help=' ')

    return local_parser

def _parse_calllable(callableobj, skipargs=[], parse_pos_args=False, 
                     parser=BASE_GLOBAL_PARSER,
                     eval_action=EvalArgParseAction, name=None, prfx=''):
    assert callable(callableobj), 'Not callabled object!!!'

    final_kwargs, final_required_args = ___parse_args(callableobj, skipargs=skipargs)
    parser_name = callableobj.__name__ if name is None  else name
    local_parser = ___prep_parser(parser=parser,
                                  final_kwargs=final_kwargs,
                                  final_required_args=final_required_args,
                                  name=parser_name, docstring=callableobj.__doc__,
                                  parse_pos_args=parse_pos_args,
                                  eval_action=eval_action, prfx=prfx)
    
    return local_parser, final_required_args
