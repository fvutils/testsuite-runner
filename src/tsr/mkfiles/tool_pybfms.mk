#********************************************************************
#* tsr_tool_pybfms.mk
#********************************************************************

# TODO: move this to a plugin in PyBFMS

ifneq (1,$(RULES))

TSR_BUILD_PRECOMPILE_TARGETS += gen-pybfms

TSR_VPI_LIBRARIES += $(shell $(TSR_PYTHON) -m pybfms lib --vpi)
TSR_DPI_OBJS_LIBS += $(shell $(TSR_PYTHON) -m pybfms lib --dpi)

PYBFMS_LIBDIR = $(dir $(shell $(TSR_PYTHON) -m pybfms lib --vpi))

LD_LIBRARY_PATH:=$(PYBFMS_LIBDIR):$(LD_LIBRARY_PATH)
export LD_LIBRARY_PATH

#DPI_LDFLAGS += -L$(shell python3-config --prefix)/lib $(shell python3-config --libs)

# TODO: Add different files based on simulator capabilities?
ifeq (systemverilog,$(SIM_LANGUAGE))
PYBFMS_LANGUAGE=sv
TSR_VLOG_ARGS_HDL += $(BUILD_DIR)/pybfms.sv $(BUILD_DIR)/pybfms.c
else
ifeq (verilog,$(SIM_LANGUAGE))
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

endif

