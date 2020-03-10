#****************************************************************************
#* tsr_engine_vlsim.mk
#*
#* Build and run definitions and rules for using the vlsim Verilator wrapper
#*
#* +tool.sim.codecov
#*
#****************************************************************************

# TODO: relocate to vlsim package

TSR_MKFILES_DIR:=$(shell $(TSR_PYTHON) -m tsr config-mkfiles)

#********************************************************************
#* Compile rules
#********************************************************************

ifneq (1,$(RULES))

include $(TSR_MKFILES_DIR)/hdlsim_common.mk

VALGRIND_ENABLED:=$(call have_plusarg,tool.vl.valgrind,$(TSR_PLUSARGS))
CODECOV_EN:=$(call have_plusarg,tool.sim.codecov,$(TSR_PLUSARGS))
TRACE_VCD:=$(call have_plusarg,tool.vlsim.tracevcd,$(TSR_PLUSARGS))
TRACE_FST:=$(call have_plusarg,tool.vlsim.tracefst,$(TSR_PLUSARGS))

ifeq (true,$(CODECOV_EN))
  TSR_VLOG_FLAGS += --coverage
endif


ifeq (true,$(TRACE_VCD))
  TRACE_FLAGS += --trace
else
  TRACE_FLAGS += --trace-fst
endif

ifeq (ms,$(findstring ms,$(TSR_TIMEOUT)))
  timeout=$(shell expr $(subst ms,,$(TSR_TIMEOUT)) '*' 1000000)
else
  ifeq (us,$(findstring us,$(TSR_TIMEOUT)))
    timeout=$(shell expr $(subst ns,,$(TSR_TIMEOUT)) '*' 1000)
  else
    ifeq (ns,$(findstring ns,$(TSR_TIMEOUT)))
      timeout=$(shell expr $(subst ns,,$(TSR_TIMEOUT)) '*' 1)
    else
      ifeq (s,$(findstring s,$(TSR_TIMEOUT)))
        timeout=$(shell expr $(subst s,,$(TSR_TIMEOUT)) '*' 1000000000)
      else
        timeout=error: unknown $(TSR_TIMEOUT)
      endif
    endif
  endif
endif

#********************************************************************
#* Capabilities configuration
#********************************************************************
# VLOG_FLAGS += +define+HAVE_HDL_VIRTUAL_INTERFACE
# VLOG_FLAGS += +define+HAVE_DPI
#VLOG_DEFINES += HAVE_HDL_DUMP HAVE_HDL_CLKGEN

SIM_LANGUAGE=systemverilog

BUILD_COMPILE_TARGETS += vlsim_compile

ifeq (,$(TB_MODULES))
ifneq (,$(TB_MODULES_HDL))
TB_MODULES = $(TB_MODULES_HDL) $(TB_MODULES_HVL)
else
TB_MODULES = $(TB)
endif
endif

ifeq (true,$(QUIET))
REDIRECT:= >simx.log 2>&1
else
REDIRECT:=2>&1 | tee simx.log
endif

RUN_TARGETS += vlsim_run

ifneq (,$(DPI_OBJS_LIBS))
# DPI_LIBRARIES += $(BUILD_DIR_A)/dpi
# LIB_TARGETS += $(BUILD_DIR_A)/dpi$(DPIEXT)
endif

ifeq ($(OS),Windows)
DPI_SYSLIBS += -lpsapi -lkernel32 -lstdc++ -lws2_32
else
DPI_SYSLIBS += -lstdc++
endif

VLOG_FLAGS += $(foreach d,$(VLOG_DEFINES),+define+$(d))
VLOG_FLAGS += $(foreach i,$(VLOG_INCLUDES),+define+$(call native_path,$(i)))

VOPT_FLAGS += -dpiheader $(TB)_dpi.h

VLOG_ARGS_PRE += $(VLOG_ARGS_PRE_1) $(VLOG_ARGS_PRE_2) $(VLOG_ARGS_PRE_3) $(VLOG_ARGS_PRE_4) $(VLOG_ARGS_PRE_5)

ifeq (,$(VLOG_ARGS_HDL))
ifneq (,$(wildcard $(SIM_DIR)/scripts/vlog_$(SIM)_hdl.f))
VLOG_ARGS_HDL += -f $(SIM_DIR_A)/scripts/vlog_$(SIM)_hdl.f
else
VLOG_ARGS_HDL += -f $(SIM_DIR_A)/scripts/vlog_hdl.f
endif
endif


DPI_LIB_OPTIONS := -ldflags "$(foreach l,$(DPI_OBJS_LIBS),$(BUILD_DIR_A)/$(l)) $(DPI_SYSLIBS)"
VOPT_OPT_DEPS += $(DPI_OBJS_LIBS)
VOPT_DBG_DEPS += $(DPI_OBJS_LIBS)

else # Rules

.phony: vopt_opt vopt_dbg vlog_compile

VLOG_FLAGS += $(foreach clk,$(VLSIM_CLOCKSPEC),-clkspec $(clk))

ifneq (,$(VPI_LIBRARIES))
#    VLOG_FLAGS += --vpi --public-flat-rw
    VLOG_FLAGS += --vpi
endif

vlsim_compile : $(DPI_OBJS_LIBS)
	$(Q)$(TSR_PYTHON) -m vlsim -sv $(TRACE_FLAGS) --top-module $(TB_MODULES_HDL) -Wno-fatal \
		$(foreach l,$(DPI_OBJS_LIBS),-LDFLAGS "-L$(dir $(abspath $(l)))") \
		$(foreach l,$(DPI_OBJS_LIBS),-LDFLAGS "-l$(subst .so,,$(subst lib,,$(notdir $(l))))") \
		-LDFLAGS "$(DPI_LDFLAGS)" \
		$(VLOG_FLAGS) $(VLOG_ARGS_HDL) \
	
ifeq (true,$(VALGRIND_ENABLED))
  VALGRIND=valgrind --tool=memcheck 
endif

ifeq (true,$(DEBUG))
RUN_ARGS += +vlsim.trace
endif

vlsim_run :
	$(Q)filelist-flatten -o arguments.txt -f sim.f $(RUN_ARGS)
	$(Q)$(RUN_ENV_VARS_V)$(BUILD_DIR)/simv \
		--public-flat-rw \
		+vlsim.timeout=$(TIMEOUT) \
		+TESTNAME=$(TESTNAME) \
		$(foreach v,$(VPI_LIBRARIES),+vpi=$(abspath $(v))) \
		`cat arguments.txt` $(REDIRECT)
		
vlsim-info:
	@echo "vlsim (Verilator wrapper)"
	
vlsim-plusargs : hdlsim-plusargs
	@echo "+tool.vlsim.tracevcd - Enable tracing in VCD format"
	@echo "+tool.vlsim.tracefst - Enable tracing in FST format (default)"

include $(TSR_MKFILES_DIR)/hdlsim_common.mk

endif # Rules

