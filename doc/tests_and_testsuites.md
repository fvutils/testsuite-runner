
Tests can be specified in several ways:
- Test .f file in the tests sub-directory
- Test-set .tset file (Python-config format) 

[base]
abstract = True
extends = base-test name
plusargs = 

[my_test1]
extends = base
plusargs = +my_control=1

[my_test2]
extends = base
plusargs = +my_control=2