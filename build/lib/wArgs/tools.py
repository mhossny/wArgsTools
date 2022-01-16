#!/Users/mo/anaconda3/bin/python
from .core import _parse_calllable, ___parse_args, ___prep_parser, EvalArgParseAction
from .core import BASE_BASE_GLOBAL_PARSER, BASE_GLOBAL_PARSER
from .core import struct, localparams
from pdb import set_trace
from collections import OrderedDict

import sys
import pdb

def make_wArgsParser(callableobj, parser=BASE_GLOBAL_PARSER,
                     eval_action=EvalArgParseAction,
                     parse_pos_args=False,
                     skipargs=[],
                     recursive=True, name=None, prfx=''):
    thisparser, pos_args = _parse_calllable(callableobj,
                                            parser=parser,
                                            parse_pos_args=parse_pos_args,
                                            eval_action=eval_action,
                                            skipargs=skipargs, name=name, prfx=prfx)
    return thisparser, pos_args


def parse_wArgs(callableobj, parser=BASE_GLOBAL_PARSER,
                eval_action=EvalArgParseAction,
                parse_pos_args=False,
                skipargs=[],
                recursive=True, unknown_args=[], validate=False, name=None, prfx=''):

    thisparser, pos_args = make_wArgsParser(callableobj, parser=parser,
                                            eval_action=eval_action,
                                            parse_pos_args=parse_pos_args,
                                            skipargs=skipargs, name=name,
                                            recursive=recursive, prfx=prfx)
    thisargs, unknown_args = thisparser.parse_known_args()

    return thisargs, unknown_args


def call_wArgs(callableobj, *args, parser=BASE_GLOBAL_PARSER,
               eval_action=EvalArgParseAction,
               skipargs=[], parse_pos_args=False,
               recursive=True, unknown_args=[], validate=False, prfx='', name=None, **kwargs):

    thisargs, unknown_args = parse_wArgs(callableobj,
                                         parser=parser,
                                         eval_action=eval_action,
                                         skipargs=skipargs,
                                         parse_pos_args=parse_pos_args,
                                         recursive=recursive, name=name,
                                         unknown_args=unknown_args, prfx=prfx)

    return_value = callableobj(*args, **vars(thisargs), **kwargs)
    return return_value


def make_wArgs(callableobj, *args, parser=BASE_GLOBAL_PARSER,
               eval_action=EvalArgParseAction,
               skipargs=[], parse_pos_args=False,
               recursive=True, unknown_args={},
               validate=False, name=None, prfx='', **kwargs):
    # Build SubArgParsers and accumulate in BASE_GLOBAL_PARSER
    make_wArgsParser(callableobj, parser=parser,
                     eval_action=eval_action,
                     parse_pos_args=parse_pos_args,
                     skipargs=skipargs,
                     recursive=recursive, prfx=prfx, name=name)

    def fun(*args, **kwargs):
        return call_wArgs(callableobj, *args, parser=parser,
                          eval_action=eval_action,
                          skipargs=skipargs,
                          parse_pos_args=parse_pos_args,
                          recursive=recursive, unknown_args=unknown_args,
                          validate=validate, **kwargs)

    fun.__name__ = '{}_wArgs'.format(callableobj.__name__)
    fun.__qualname__ = fun.__name__
    return fun


def makeC_wArgs_Ex(callableobj, *args, parser=BASE_GLOBAL_PARSER,
                   eval_action=EvalArgParseAction,
                   parse_pos_args=False,
                   skipargs=[], ignore_python_object=True,
                   recursive=True, unknown_args={}, name=None, prfx=''):
    # Build SubArgParsers and accumulate in BASE_GLOBAL_PARSER

    docstring = ''
    pos_args = []
    final_kwargs, final_required_args = {}, []
    for cobj in reversed(callableobj.mro()):
        if cobj is object: continue
        
        these_kwargs, these_required_args = ___parse_args(cobj, skipargs=skipargs)

        # set_trace()
        final_kwargs.update(these_kwargs)
        if parse_pos_args:
            pos_args += these_required_args

        docstring += f'`{cobj.__name__}`: {cobj.__doc__}\n'

    tmp_prep_parser = ___prep_parser
    parser_name = callableobj.__name__ if name is None else name

    prepared_parser = tmp_prep_parser(parser=parser,
                                      final_kwargs=final_kwargs,
                                      final_required_args=pos_args,
                                      name=parser_name, docstring=docstring, 
                                      parse_pos_args=parse_pos_args,
                                      eval_action=eval_action, prfx=prfx)

    # Build a callable class encapsulating callableobj
    class tmp(callableobj):
        def __init__(self, *args, **kwargs):
            self.parser = prepared_parser
            self.parsed_args, self.unknown_args = self.__parse_args()
            pos_args_kw = {k: None for k in pos_args[len(args):]}

            passed_kwargs = OrderedDict()
            passed_kwargs.update(pos_args_kw)
            passed_kwargs.update(kwargs)
            passed_kwargs.update(vars(self.parsed_args))

            # set_trace()
            args = [] if parse_pos_args else args
            #pdb.set_trace()

            callableobj.__init__(self, *args, **passed_kwargs)
            '''
            if not __debug__:
                callableobj.__init__(self, *args, **passed_kwargs)
            else:
                print('DEBUG')
                try:
                    callableobj.__init__(self, *args, **passed_kwargs)
                except:
                    print('(E) INSIDE wArgsClass. A sub-class is missing **kwargs to parent class.')
                    raise Exception('(E) INSIDE wArgsClass. A sub-class is missing **kwargs to parent class.')
            #'''
            pass

        def __parse_args(self, unknown_args=[]):
            parsed_args, unknown_args = self.parser.parse_known_args()
            return parsed_args, unknown_args

    # Give it a pretty name
    tmp.__name__ = '{}_wArgs_{}'.format(callableobj.__name__, prfx)
    tmp.__qualname__ = tmp.__name__
    return tmp


def hlp_wArgs_(parser=BASE_GLOBAL_PARSER):
    for i, (parsername, thisparser) in enumerate(parser.choices.items()):
        #set_trace()
        print(thisparser.format_help())
        print()
        this_help = ': ' + \
            ''.join(thisparser.format_help().split(parsername)[1:])
        this_help = ['Module ', this_help]
        this_help = parsername.join(this_help)

        print(this_help)


def hlp_wArgs(parser=BASE_GLOBAL_PARSER):
    for i, (parsername, thisparser) in enumerate(parser.choices.items()):
        print(thisparser.format_help())


def __chk_wArgs(warn=False, print_argv=False, parser=BASE_GLOBAL_PARSER, argv=sys.argv, stay=False):
    def argdtl(args):
        if len(args) == 0:
            return {}, '', []

        argd = {arg.split()[0]: arg.split()[1:]
                for arg in ' '.join(args).split('--')}
        argt = ' '.join([''.join(['--']+[k]+[' ']+v) for k, v in argd.items()])
        argl = list(argd.keys())
        return argd, argt, argl

    if print_argv:
        print(' '.join(argv))

    if '-h' in argv or '--help' in argv:
        hlp_wArgs(parser)
        if not stay:
            exit(0)

    known_args = []
    argd, argt, argl = argdtl(' '.join(argv))
    pdb.set_trace()
    pass
    
    
def chk_wArgs(warn=False, print_argv=False, parser=BASE_GLOBAL_PARSER, argv=sys.argv, stay=False, skip_warn=False):
    if print_argv:
        print(' '.join(argv))

    if '-h' in argv or '--help' in argv:
        hlp_wArgs(parser)
        if not stay:
            exit(0)

    known_args = []
    for i, (parsername, thisparser) in enumerate(parser.choices.items()):
        print(parsername)
        #pdb.set_trace()
        these_args, unknown_args = thisparser.parse_known_args()

        #pdb.set_trace()
        metavars = [a.option_strings[0] for a in thisparser._actions if a.dest is not None]
        #metavars = ['--' + a.dest for a in thisparser._actions if a.dest is not None]
        args = {a: v for a, v in vars(these_args).items() if type(v) is not bool}

        #pdb.set_trace()
        
        # TODO: Use Levenshtein Distance and argmax
        ka = [[list(filter(lambda x: x[2:]==a, metavars))[0], str(v)] for a, v in args.items()
              if any(map(lambda x: x[2:]==a, metavars))]
        bka = [[list(filter(lambda x: x[2:]==a, metavars))[0], v] for a, v in vars(these_args).items()
               if any(map(lambda x: x[2:]==a, metavars)) and type(v) is bool]
        known_args += ka + bka

        ka = [[list(filter(lambda x: x.endswith(a), metavars))[0], str(v)] for a, v in args.items()
              if any(map(lambda x: x.endswith(a), metavars))]
        bka = [[list(filter(lambda x: x.endswith(a), metavars))[0], v] for a, v in vars(these_args).items()
               if any(map(lambda x: x.endswith(a), metavars)) and type(v) is bool]
        known_args += ka + bka

        if parsername == 'DDPGAgent': #'Actor':
            #pdb.set_trace()
            pass
        #print(known_args)[<8;76;45m
    # TODO: There is a special case here for floating numbers str(#) opts for scientific notation
    # Issuing a warning at the moment
    # TODO: Does not detect additioinal unjustiified values
    import numpy as np
    known_args = np.array(known_args).flatten().tolist()

    def argdtl(args):
        if len(args) == 0:
            return {}, '', []

        #pdb.set_trace()
        argd = {arg.split()[0]: arg.split()[1:]
                for arg in ' '.join(args).split('--')}
        argt = ' '.join([''.join(['--']+[k]+[' ']+v) for k, v in argd.items()])
        argl = list(argd.keys())
        return argd, argt, argl

    def smart_eval(v):
        # TODO: VERY UGLY
        from ast import literal_eval
        try:
            #return '{}'.format(literal_eval(v))
            return '{}'.format(eval(v))
        except:
            return v

    known_argd, argt, argl = argdtl(['dummy'] + known_args)
    unknown_argd, argt, argl = argdtl(['dummy'] + unknown_args)
    unknown_argd = {k: v for k, v in unknown_argd.items() if k not in known_argd}
    
    #pdb.set_trace()
    unknown_args = [f'--{k}'for k in unknown_argd]  # [a for a in unknown_args if smart_eval(a) not in known_args]

    #pdb.set_trace()
    if len(unknown_args) > 0:
        if warn:
            if not skip_warn:
                errmsg = '(W) Unrecognised argument(s): '
                print(errmsg, *unknown_args)
        else:
            hlp_wArgs(parser)
            errmsg = '(E) Unrecognised argument(s): '
            print(errmsg, *unknown_args)
            print()
            exit(-1)


def chk_wArgs_(print_argv=False, parser=BASE_GLOBAL_PARSER, argv=sys.argv):
    if print_argv:
        print(' '.join(argv))

    if '-h' in argv or '--help' in argv:
        hlp_wArgs(parser)
        exit(0)

    known_args = []
    for i, (parsername, thisparser) in enumerate(parser.choices.items()):
        these_args, unknown_args = thisparser.parse_known_args()

        print(parsername)
        pdb.set_trace()
        # reformat keys
        known_args += ['--%s' % k for k in vars(these_args).keys()]

        # reformat values except iterables (exclude str)
        known_args += [str(v) for v in vars(these_args).values()
                       if type(v) is str or not hasattr(v, '__iter__')]

        # reformat and append iterables (exlude str)
        iterables = [v for v in vars(these_args).values()
                     if type(v) is not str and hasattr(v, '__iter__')]
        for this_iterable in iterables:
            known_args += [str(v) for v in this_iterable]

    # TODO: There is a special case here for floating numbers str(#) opts for scientific notation
    # Issuing a warning at the moment
    unknown_args = [a for a in unknown_args if a not in known_args]

    if len(unknown_args) > 0:
        errmsg = '(W) Unrecognised argument(s): '
        print(errmsg, *unknown_args)
        print()
        
def wildArgs(**kwargs):
    wildArgs._id += 1
    lambda_kwargs_txt = ','.join([f'{k}={v}' for k, v in kwargs.items() if type(v) is not str])
    lambda_kwargs_txt += ',' + ','.join([f'{k}="{v}"' for k, v in kwargs.items() if type(v) is str])
    fun = eval(f'lambda {lambda_kwargs_txt}: locals()')
    
    return struct(**call_wArgs(fun, name=f'wildArgs_{wildArgs._id:02d}'))
wildArgs._id = -1

        
def mkWildArgs(**kwargs):
    wildArgs._id += 1
    lambda_kwargs_txt = ','.join([f'{k}={v}' for k, v in kwargs.items() if type(v) is not str])
    lambda_kwargs_txt += ',' + ','.join([f'{k}="{v}"' for k, v in kwargs.items() if type(v) is str])
    fun = eval(f'lambda {lambda_kwargs_txt}: locals()')
    
    return make_wArgs(fun, name=f'wildArgs_{wildArgs._id:02d}')
mkWildArgs._id = -1
