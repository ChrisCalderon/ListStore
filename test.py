from serpent_tests import Tester

def main():
    myTest = Tester('liststore.se')
    owner = myTest.accounts[0].address_as_int
    vals = range(1, 11)
    tests = (('addVal', (1, 1337), {}, 1),
             ('getList', (owner, 1), {}, [1337]),
             ('getMyList', (1,), {}, [1337]),
             ('addVals', (1, vals), {}, 1),
             ('getMyList', (1,), {}, [1337] + vals),
             ('isMember', (owner, 1, 1337), {}, 1),
             ('isMember', (owner, 1, 11), {}, 0),
             ('remove', (1, 1337), {}, 1),
             ('remove', (1, 1337), {}, 0),
             ('getList', (owner, 1), {}, [0] + vals),
             ('replace', (1, 5, 1337), {}, 1),
             ('getMyList', (1,), {}, [0] + [1,2,3,4,1337,6,7,8,9,10]),
             ('addVal', (1, 27), {}, 1),
             ('getMyList', (1,), {}, [27,1,2,3,4,1337,6,7,8,9,10]))
    myTest.run_tests(tests)

if __name__ == '__main__':
    main()
