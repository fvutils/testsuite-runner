
tsr-config.json
- Specifies project settings
  - Project name
  - tools: Tools needed by the project
  - variables
  - engines : map
    - default: 
    - supported: map
      - <engine> : map
        - variables
    - 

Tests are specified using .json files located in specific directories.

- test-group
  - name
  - variables - list of variables
    - <varname> - value or list of values to append to <varname>
  - tests : list
    - test : set
      - name
      - variables
        - <varname>
      - variables

Test suite specification must handle two use cases
- Collect tests together to run
- Specify the engine (or engines) under which those tests should run

Test
Group
Suite
Regression (?)

- Specify parameters for individual test
- Group tests based on commonalities
- Specify suites of tests to run -- possibly multiple times, with different seeds, etc
- Specify multi-engine regressions composed 

test-suite
  - name
  - Note: must provide a way to specify 
  - tests - list of specs for test to include
    - include
      - name or pattern
      - set




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