from wArgs import wArgs, wArgsCall, wArgsChk, wArgsInit

pi= 22./7.

wArgsInit(globals())

def myfunc(x, y, z, a=12, b='abc', flag=False, eval=None, Correct=True):
    '''
    This function is just awesome!!!!! 
    It uses <x, y, z> as spatial coordinates for 
    the system while [a, b] for parameter tuning. 
    `flag` allows moementum and `eval` accetps 
    python code.
    '''
    print(f'x={x}')
    print(f'y={y}')
    print(f'z={z}')
    print(f'a={a}')
    print(f'b={b}')
    print(f'flag={flag}')
    print(f'Correct={flag}')
    print(f'eval={eval}')


# Lazy Call
fun_wArgs = wArgs(myfunc, parse_pos_args=True)
wArgsChk()

    
fun_wArgs()
