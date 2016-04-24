import warnings; warnings.simplefilter('ignore')
from ethereum import tester as t
from ethereum import utils
import sys
from colorama import Fore, Style, init; init()

passed = Fore.GREEN + 'passed' + Style.RESET_ALL
failed = Style.BRIGHT + Fore.RED + 'failed' + Style.RESET_ALL

def test(func, args, expected):
    sys.stdout.write('testing {}: '.format(func.__name__))
    sys.stdout.flush()
    result = func(*args)
    if result == expected:
        print passed
    else:
        arg_str = ', '.join(map(str, args))
        print failed
        print '  {}({}) => {}'.format(func.__name__, arg_str, result)
        print '  expected {}'.format(expected)
        sys.exit(1)

def abi_to_int(s):
    if s == '':
        return 0
    return abi_to_int(s[:-1])<<8 | ord(s[-1])

s = t.state()
c = s.abi_contract('liststore.se')
owner = abi_to_int(t.a0)
vals = range(1,11)

for name, thing in vars(c).items():
    if getattr(thing, '__name__', '') == 'kall':
        thing.__name__ = str(name)

tests = ((c.addVal, (1, 1337), 1),
         (c.getList, (owner, 1), [1337]),
         (c.getMyList, (1,), [1337]),
         (c.addVals, (1, vals), 1),
         (c.getMyList, (1,), [1337] + vals),
         (c.isMember, (owner, 1, 1337), 1),
         (c.isMember, (owner, 1, 11), 0),
         (c.remove, (1, 1337), 1),
         (c.remove, (1, 1337), 0),
         (c.getList, (owner, 1), [0] + vals),
         (c.replace, (1, 5, 1337), 1),
         (c.getMyList, (1,), [0] + [1,2,3,4,1337,6,7,8,9,10]),
         (c.addVal, (1, 27), 1),
         (c.getMyList, (1,), [27,1,2,3,4,1337,6,7,8,9,10]))

for func, args, exp in tests:
    test(func, args, exp)
    s.mine(1)
