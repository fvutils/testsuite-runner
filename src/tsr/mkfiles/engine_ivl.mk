#****************************************************************************
#* tsr_engine_ivl.mk
#*
#* Build and run definitions and rules for Icarus Verilog
#*
#*
#****************************************************************************

#TSR_MKFILES_DIR:=$($(TSR_PYTHON) -m tsr config-mkfiles)
TSR_MKFILES_DIR:=$(dir $(lastword $(MAKEFILE_LIST)))

#********************************************************************
#* Compile rules
#********************************************************************

ifneq (1,$(RULES))

include $(TSR_MKFILES_DIR)/hdlsim_common.mk


ifeq (ms,$(findstring ms,$(TIMEOUT)))
  timeout=$(shell expr $(subst ms,,$(TIMEOUT)) '*' 1000000)
else
  ifeq (us,$(findstring us,$(TIMEOUT)))
    timeout=$(shell expr $(subst us,,$(TIMEOUT)) '*' 1000)
  else
    ifeq (ns,$(findstring ns,$(TIMEOUT)))
      timeout=$(shell expr $(subst ns,,$(TIMEOUT)) '*' 1)
    else
      ifeq (s,$(findstring s,$(TIMEOUT)))
        timeout=$(shell expr $(subst s,,$(TIMEOUT)) '*' 1000000000)
      else
        timeout=error: unknown $(TIMEOUT)
      endif
    endif
  endif
endif

#********************************************************************
#* Capabilities configuration
#********************************************************************
TSR_VLOG_DEFINES += HAVE_HDL_DUMP HAVE_HDL_CLKGEN IVERILOG

SIM_LANGUAGE=verilog

BUILD_COMPILE_TARGETS += ivl_compile

ifeq (,$(TB_MODULES))
ifneq (,$(TB_MODULES_HDL))
TB_MODULES = $(TB_MODULES_HDL) $(TB_MODULES_HVL)
else
TB_MODULES = $(TB)
endif
endif

TSR_RUN_TARGETS += ivl_run

TSR_VLOG_FLAGS += $(foreach d,$(TSR_VLOG_DEFINES),-D $(d))
TSR_VLOG_FLAGS += $(foreach i,$(TSR_VLOG_INCLUDES),-I $(call native_path,$(i)))

else # Rules

#********************************************************************
#* Query interface to provide engine-specific details
#********************************************************************
ivl-help: ivl-info ivl-plusargs

ivl-info:
	@echo "Icarus Verilog"
	
ivl-plusargs: hdlsim-plusargs
	
#********************************************************************
#* Build/Run rules
#********************************************************************

ivl_compile : 
	$(Q)iverilog -g2009 -o simv.vvp -s $(TSR_TB_MODULES_HDL) $(TSR_VLOG_FLAGS) $(TSR_VLOG_ARGS_HDL)

TSR_RUN_ARGS += +timeout=$(timeout)
	
ifeq (true,$(DEBUG))
TSR_RUN_ARGS += +dumpvars
endif

ivl_run :
	$(Q)$(TSR_RUN_ENV_VARS_V)vvp \
		$(foreach l,$(VPI_LIBRARIES),-m $(l)) \
		$(TSR_RUN_FLAGS) \
		$(TSR_BUILD_DIR)/simv.vvp \
		$(TSR_RUN_ARGS) $(REDIRECT)
		
include $(TSR_MKFILES_DIR)/hdlsim_common.mk
	
endif # Rules

