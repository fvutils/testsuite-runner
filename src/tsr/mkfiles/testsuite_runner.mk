
TSR_MKFILES_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
TSR_DIR := $(abspath $(TSR_MKFILES_DIR)/..)

include $(TSR_DIR)/mkfiles/plusargs.mk

TOP_MODULE ?= $(TB)
DEBUG ?= false

# RUN_ARGS

# Timeout selection
# - Test-specific timeout
# - Project-specific timeout
# - 1ms
TEST_TIMEOUT := $(call get_plusarg,TIMEOUT,$(PLUSARGS))
TEST_SEED := $(call get_plusarg,seed,$(PLUSARGS))

ifneq (,$(TEST_SEED))
SEED := $(TEST_SEED)
endif

ifneq (,$(TEST_TIMEOUT))
TIMEOUT := $(TEST_TIMEOUT)
else
TIMEOUT ?= 1ms
endif

COMMON_SIM_MK := $(lastword $(MAKEFILE_LIST))
COMMON_SIM_MK_DIR := $(dir $(COMMON_SIM_MK))
export COMMON_SIM_MK_DIR


DLLEXT=.so
LIBPREF=lib

RUN_ENV_VARS_V=$(foreach v,$(RUN_ENV_VARS),export $(v);)

ifeq (,$(DEFAULT_SIM))
SIM:=qs
else
SIM:=$(DEFAULT_SIM)
endif

include $(COMMON_SIM_MK_DIR)/common_defs.mk

# Locate the simulator-support file
# - Don't include a simulator-support file if SIM='none'
# - Allow the test suite to provide its own
# - Allow the environment to provide its own
# - Finally, check if 'simscripts' provides an implementation
ifneq (,$(TSR_ENGINE_MK))
MK_INCLUDES += $(TSR_ENGINE_MK)
endif

ifneq (,$(TSR_TOOL_MK))
MK_INCLUDES += $(TSR_TOOL_MK)
endif

# Filter out tool-control options like +tool.foo.setting_bar=XXX
TSR_PLUSARGS_TOOLS := $(sort $(patsubst +tool.%,%,$(filter +tool.%,$(shell echo $(PLUSARGS) | sed -e 's/\+tool\.[a-zA-Z][a-zA-Z0-9_]*\.[a-zA-Z][a-zA-Z0-9_\.]*//g'))))

# Build a full list of tools to bring in
TSR_TOOLS += $(TSR_PLUSARGS_TOOLS)

# Include tool-specific makefiles
MK_INCLUDES += $(foreach tool,$(TSR_TOOLS),$(TSR_DIR)/mkfiles/common_tool_$(tool).mk)
MK_INCLUDES += $(TSR_DIR)/mkfiles/common_tool_gcc.mk

include $(MK_INCLUDES)

DPIEXT=$(DLLEXT)

#BUILD_TARGETS += build-pre-compile build-compile build-post-compile build-pre-link
BUILD_TARGETS += build-post-link	
BUILD_LINK_TARGETS += $(LIB_TARGETS) $(EXE_TARGETS)
	

post_build : $(POSTBUILD_TARGETS)
	if test "x$(TARGET_MAKEFILE)" != "x"; then \
		$(MAKE) -f $(TARGET_MAKEFILE) build; \
	fi



LD_LIBRARY_PATH := $(BUILD_DIR)/libs:$(LD_LIBRARY_PATH)

LD_LIBRARY_PATH := $(foreach path,$(BFM_LIBS),$(dir $(path)):)$(LD_LIBRARY_PATH)
export LD_LIBRARY_PATH

RULES := 1

.phony: all build run target_build
.phony: pre-run post-run

all :
	echo "Error: Specify target of build or run
	exit 1
	
# Build Targets
# - Pre-Compile
# - Compile
# - Post-Compile
# - Pre-Link
# - Link
# - Post-Link

build-pre-compile : $(BUILD_PRECOMPILE_TARGETS)
	@touch $@

build-compile : build-pre-compile $(BUILD_COMPILE_TARGETS)
	@touch $@
	
$(BUILD_COMPILE_TARGETS) : build-pre-compile

build-post-compile : build-compile $(BUILD_POSTCOMPILE_TARGETS)
	@touch $@
	
$(BUILD_POSTCOMPILE_TARGETS) : build-compile

build-pre-link : build-post-compile $(BUILD_PRELINK_TARGETS)
	@touch $@
	
$(BUILD_PRELINK_TARGETS) : build-post-compile

build-link : build-pre-link $(BUILD_LINK_TARGETS)
	@touch $@
	
$(BUILD_LINK_TARGETS) : build-pre-link

build-post-link : build-link $(BUILD_POSTLINK_TARGETS)
	@touch $@
	
$(BUILD_POSTLINK_TARGETS) : build-link
	
# build : $(BUILD_TARGETS)
build : build-post-link
	@echo "TSR_TOOLS: $(TSR_TOOLS)"
	@echo "TSR_PLUSARGS_TOOLS: $(TSR_PLUSARGS_TOOLS)"
	@echo "PLUSARGS: $(sort $(PLUSARGS))"
	@echo "INFACT_IMPORT_TARGETS: $(INFACT_IMPORT_TARGETS)"
	@echo "build-pre-compile: $(BUILD_PRECOMPILE_TARGETS)"
	@echo "build-compile: $(BUILD_COMPILE_TARGETS)"
	@echo "build-post-compile: $(BUILD_POSTCOMPILE_TARGETS)"
	@echo "build-pre-link: $(BUILD_PRELINK_TARGETS)"
	@echo "build-link: $(BUILD_LINK_TARGETS)"
	@echo "build-post-link: $(BUILD_POSTLINK_TARGETS)"
	@touch $@

run-pre : $(RUN_PRE_TARGETS)
	$(Q)touch $@

run-main : run-pre $(RUN_TARGETS)
	$(Q)touch $@

$(RUN_TARGETS) : run-pre

run-post : run-main $(RUN_POST_TARGETS)
	$(Q)touch $@

$(RUN_POST_TARGETS) : run-main

run : run-post
	$(Q)touch $@

pre-run: init-tools $(PRE_RUN_TARGETS)

post-run: $(POST_RUN_TARGETS)

init-tools:
	@echo "== Simulator: $(SIM) == "
	@echo "== Enabled Tools =="
	@for tool in $(TSR_TOOLS); do \
		echo "  - $${tool}"; \
	done

missing_sim_mk :
	@echo "Error: Failed to find makefile for sim $(SIM) in \$$(TSR_DIR)/mkfiles/sim_mk and \$$(TSR_DIR)/../mkfiles"
	@exit 1

include $(MK_INCLUDES)
include $(COMMON_SIM_MK_DIR)/common_rules.mk

