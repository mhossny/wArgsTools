#!/Users/mo/anaconda3/bin/python

#import IPython; IPython.embed()
from .. import wArgs, wArgsHelp, wArgsCheck, wArgsClass

import pdb

class A(object):
    def __init__(self, d, x=1, y=.1, name='sss', *args, **kwargs):
        print(locals())
        pass
    
    def create_f1(self, a='a', b=.1, c=12):
        print('f1:', a, b, c)

    
class B(A):
    def __init__(self, newperson, newdict, bydirection=.1,
                 newname='sss', newbvar='r', *args, tmparg, tmparg2=12, **kwargs):
        pass
    
    def create_and_train_f2(self, f2char='a', f2float=.1, f2int=12):
        return -123
        pass

# TEST CASES
test_f_empty = lambda: 0
test_f_1arg = lambda x: x
test_f_2args = lambda x, y: (x, y)
test_f_1arg_varargs = lambda x, *args: (x, *args)

test_f_1kwarg = lambda x=0: x
test_f_2kwarg = lambda x=0, y=1: (x, y)

test_f_1arg_2kwarg = lambda x, y=1, z=2: (x, y, z)
test_f_vargs_2kwarg = lambda *args, y=1, z=2: (*args, y, z)
test_f_1arg_vargs_2kwarg = lambda x, *args, y=1, z=2: (x, *args, y, z)

test_f_1arg_vargs_1kwarg = lambda x, *args, y=1, z, **kwargs: (x,
                                                               *args,
                                                               y,
                                                               z,
                                                               kwargs.values())

test_f_1arg_vargs_1kwarg_vkwargs = lambda x, *args, y=1, z, **kwargs: (x,
                                                                       *args,
                                                                       y,
                                                                       z,
                                                                       kwargs.values())

def test_f(x, y, z, *args, a, b=1, c='a', d=False,
           e=[], f=[1, 2, 3], g={'a', 'b', 'c'}, **kwargs):
    print()
    print()
    print(locals())
                                                                       
TEST_CASES = {k: v for k, v in locals().items() if k.startswith('test_')}

def test_fun(x, y, z=12, name='Marwa', c=list('ddd')):
    print(locals())


class Z(object):
    def __init__(self, zoomba, zeta1=(3, 5), eta2=('e', 55)):
        pass
    
class AA(B, Z):
    def __init__(self, a, b=.1, c=list('sss'), d=None, *args, **kwargs):
        print(locals())
        pass

test_f_wArgs = wArgs(test_fun)
#test_A_wArgs = wArgs(AA)

test_A_wArgs = wArgsClass(AA)  # , parse_pos_args=True)

#pdb.set_trace()

wArgsCheck()
test_f_wArgs(1, 2)
test_A_wArgs(4)
