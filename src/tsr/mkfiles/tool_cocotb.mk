#********************************************************************
#* tsr_tool_cocotb.mk
#********************************************************************
SIMSCRIPTS_MKFILES_DIR:=$(dir $(lastword $(MAKEFILE_LIST)))

ifneq (1,$(RULES))

COCOTB_MODULE:=$(call get_plusarg,cocotb.module,$(PLUSARGS))
COCOTB:=$(shell $(TSR_PYTHON) -m cocotb.config --prefix)

TSR_RUN_ENV_VARS += MODULE=$(COCOTB_MODULE)
TSR_RUN_ENV_VARS += COCOTB_SIM=1

COCOTB_DPI_LIBS = libgpi.so libcocotbutils.so libgpilog.so libcocotb.so

LIB_DIR=$(COCOTB)/cocotb/libs/verilator

TSR_VPI_LIBRARIES += $(LIB_DIR)/libvpi.so
TSR_DPI_OBJS_LIBS += $(foreach l,$(COCOTB_DPI_LIBS), $(LIB_DIR)/$(l))

LD_LIBRARY_PATH:=$(LIB_DIR):$(LD_LIBRARY_PATH)
export LD_LIBRARY_PATH

TSR_DPI_LDFLAGS += -L$(shell python3-config --prefix)/lib $(shell python3-config --libs)

# Would be nice to not need to do this
PYTHONPATH:=$(LIB_DIR):$(PYTHONPATH)
export PYTHONPATH

TSR_VLOG_DEFINES += HAVE_COCOTB

else

$(foreach l,$(COCOTB_DPI_LIBS),$(BUILD_DIR)/cocotb/build/libs/x86_64/$(l)) : build-cocotb-libs

#********************************************************************
#* Build the coctb libraries
#*
#* Note: The cocotb makefiles directly reference 'gcc' and 'g++'.
#*       In order to use Conda, we need to use $(CC) and $(CXX)
#*       instead. The code below does a little switch-around, 
#*       copying and modifying the Makefiles from cocotb such that
#*       they can be used standalone, and so they reference the
#*       compilers correctly.
#********************************************************************
build-cocotb-libs :
	$(Q)$(MAKE) -f $(SIMSCRIPTS_MKFILES_DIR)/cocotb_libs.mk \
		USER_DIR=$(BUILD_DIR)/cocotb \
                -j1 vpi-libs
                
cocotb-info:
	@echo "Enables cocotb support in HDL simulator engines"

cocotb-plusargs:
	@echo ""
	
		
endif

