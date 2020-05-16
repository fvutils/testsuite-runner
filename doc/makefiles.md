
All makefiles should be referenced relative to the path returned from
`python -m tsr config-mkfiles`

testsuite_runner.mk -- Include in test Makefile
plusargs.mk -- Include to access 


# Generated makefiles
- tsr.mk            - Placed in the engine-specific build directory. Contains
                      makefile includes for the selected engine and 
                      globally-enabled tools.
                      
- variables.mk      - Placed in the build directory, and defines TSR_PLUSARGS 
                      for build-time operations
					- Placed in the test-run directory. Includes the relevant
                      tsr.mk makefile, as well as the makefiles for any 
                      test-specific tools. 