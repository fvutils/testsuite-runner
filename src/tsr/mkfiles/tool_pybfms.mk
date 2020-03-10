#********************************************************************
#* tsr_tool_pybfms.mk
#********************************************************************

# TODO: move this to a plugin in PyBFMS

ifneq (1,$(RULES))

#********************************************************************
#* Generate the HDL wrapper file for BFMs during pre-compile 
#********************************************************************
TSR_BUILD_PRECOMPILE_TARGETS += gen-pybfms

TSR_VPI_LIBRARIES += $(shell $(TSR_PYTHON) -m pybfms lib --vpi)
TSR_DPI_OBJS_LIBS += $(shell $(TSR_PYTHON) -m pybfms lib --dpi)

PYBFMS_LIBDIR = $(dir $(shell $(TSR_PYTHON) -m pybfms lib --vpi))

TSR_LIBPATH += $(PYBFMS_LIBDIR)

# TODO: Add different files based on simulator capabilities?
ifeq (systemverilog,$(TSR_HDL_LANGUAGE))
PYBFMS_LANGUAGE=sv
TSR_VLOG_ARGS_HDL += $(BUILD_DIR)/pybfms.sv $(BUILD_DIR)/pybfms.c
else
ifeq (verilog,$(TSR_HDL_LANGUAGE))
PYBFMS_LANGUAGE=vlog
TSR_VLOG_ARGS_HDL += $(BUILD_DIR)/pybfms.v
else
COCOTB_BFM_LANGUAGE=UNKNOWN-$(SIM_LANGUAGE)
endif
endif

else

#********************************************************************
#* Generate pybfms wrappers
#********************************************************************
gen-pybfms :
	$(Q)$(TSR_PYTHON) -m pybfms generate -l $(PYBFMS_LANGUAGE) \
		$(foreach m,$(PYBFMS_BFM_MODULES),-m $(m))

pybfms-info:
	@echo "Enables PyBFMS support in simulator engines"

pybfms-plusargs:
	@echo ""
		
endif

