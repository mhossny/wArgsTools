import wArgs
from wArgs import wildArgs, wArgsChk, mkWildArgs, wArgsInit


pi= 22./7.

wArgsInit(globals())

# Lazy Call
args = mkWildArgs(x=1, y=12.5, flag=False,
                list2=[4, 8], tuple3=(.0, .3, 1e-4), itr=[],
                eval=None, string='abc')

wArgsChk(warn=True)  # Check for help
print(args())
print()

