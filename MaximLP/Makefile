################################################################################
 # Copyright (C) 2016 Maxim Integrated Products, Inc., All Rights Reserved.
 #
 # Permission is hereby granted, free of charge, to any person obtaining a
 # copy of this software and associated documentation files (the "Software"),
 # to deal in the Software without restriction, including without limitation
 # the rights to use, copy, modify, merge, publish, distribute, sublicense,
 # and/or sell copies of the Software, and to permit persons to whom the
 # Software is furnished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included
 # in all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 # OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 # IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
 # OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 # ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 # OTHER DEALINGS IN THE SOFTWARE.
 #
 # Except as contained in this notice, the name of Maxim Integrated
 # Products, Inc. shall not be used except as stated in the Maxim Integrated
 # Products, Inc. Branding Policy.
 #
 # The mere transfer of this software does not imply any licenses
 # of trade secrets, proprietary technology, copyrights, patents,
 # trademarks, maskwork rights, or any other form of intellectual
 # property whatsoever. Maxim Integrated Products, Inc. retains all
 # ownership rights.
 #
 # $Date: 2020-10-21 15:17:32 -0500 (Wed, 21 Oct 2020) $ 
 # $Revision: 56456 $
 #
 ###############################################################################

MAKE=make

# This is the name of the build output file
# ** Change this!! ** 
# You need to change this to match the name of your project folder (the folder that contains this makefile).
# This is necessary for the VS Code debugger/flashing to work - it looks for compiled binaries with the name [Project folder].elf
# Ex:  
# 	The full path to this makefile is C:\Users\Jake.Carter\Projects\MyProject\Makefile, so line 44 would be PROJECT=MyProject
ifeq "$(PROJECT)" ""
PROJECT=changeme!
endif

# Specify the target processor
ifeq "$(TARGET)" ""
TARGET=MAX32665
endif

# Create Target name variables
TARGET_UC:=$(shell echo $(TARGET) | tr a-z A-Z)
TARGET_LC:=$(shell echo $(TARGET) | tr A-Z a-z)

# Select 'GCC' or 'IAR' compiler
COMPILER=GCC

# Specify the board used
ifeq "$(BOARD)" ""
BOARD=EvKit_V1
endif

# This is the path to the CMSIS root directory
ifeq "$(MAXIM_PATH)" ""
LIBS_DIR=../../../Libraries
else
LIBS_DIR=/$(subst \,/,$(subst :,,$(MAXIM_PATH))/Firmware/$(TARGET_UC)/Libraries)
endif
CMSIS_ROOT=$(LIBS_DIR)/CMSIS

ifeq ($(MAKECMDGOALS),sla)
SECURE_BOOT_TOOLS_DIR=$(LIBS_DIR)/../NDALibraries/SecureBootTools
CA_SIGN_BUILD=$(SECURE_BOOT_TOOLS_DIR)/script/sign_application.sh
BUILD_SESSION=$(SECURE_BOOT_TOOLS_DIR)/script/build_application.sh
TEST_KEY=$(SECURE_BOOT_TOOLS_DIR)/key/maximtestcrk.key
endif

# Source files for this test (add path to VPATH below)
SRCS  = main.c
ifeq ($(MAKECMDGOALS),sla)
SRCS += sla_header.c
endif
# Where to find source files for this test
VPATH=.
ifeq ($(MAKECMDGOALS),sla)
VPATH += $(SECURE_BOOT_TOOLS_DIR)/sla_header
endif
# Where to find header files for this test
IPATH = .

# Enable assertion checking for development
PROJ_CFLAGS+=-DMXC_ASSERT_ENABLE 

# Specify the target revision to override default
# "A2" in ASCII
# TARGET_REV=0x4132

# Use this variables to specify and alternate tool path
#TOOL_DIR=/opt/gcc-arm-none-eabi-4_8-2013q4/bin

# Use these variables to add project specific tool options
#PROJ_CFLAGS+=--specs=nano.specs
#PROJ_LDFLAGS+=--specs=nano.specs

# Point this variable to a startup file to override the default file
#STARTUPFILE=start.S

# Set MXC_OPTIMIZE to override the default optimization level 
MXC_OPTIMIZE=-O1

# Point this variable to a linker file to override the default file
#LINKERFILE=$(CMSIS_ROOT)/Device/Maxim/$(TARGET_UC)/Source/GCC/$(TARGET_LC).ld
ifeq ($(MAKECMDGOALS),sla)
LINKERFILE=$(SECURE_BOOT_TOOLS_DIR)/linker/$(TARGET_LC)_sla.ld
endif
################################################################################
# Include external library makefiles here

# Include the BSP
BOARD_DIR=$(LIBS_DIR)/Boards/$(BOARD)
include $(BOARD_DIR)/board.mk

# Include the peripheral driver
PERIPH_DRIVER_DIR=$(LIBS_DIR)/$(TARGET_UC)PeriphDriver
include $(PERIPH_DRIVER_DIR)/periphdriver.mk

################################################################################
# Include the rules for building for this target. All other makefiles should be
# included before this one.
include $(CMSIS_ROOT)/Device/Maxim/$(TARGET_UC)/Source/$(COMPILER)/$(TARGET_LC).mk

# The rule to clean out all the build products.
distclean: clean
	$(MAKE) -C ${PERIPH_DRIVER_DIR} clean
	rm -rf scp_packets


sla: all
	arm-none-eabi-objcopy $(BUILD_DIR)/$(PROJECT).elf -R .sig -O binary $(BUILD_DIR)/$(PROJECT).bin
	$(CA_SIGN_BUILD) $(BUILD_DIR)/$(PROJECT).bin $(TEST_KEY)
	arm-none-eabi-objcopy  $(BUILD_DIR)/$(PROJECT).elf --update-section .sig=$(BUILD_DIR)/$(PROJECT).bin.sig
	arm-none-eabi-objcopy $(BUILD_DIR)/$(PROJECT).elf -O binary $(BUILD_DIR)/$(PROJECT).bin.sbin
	$(BUILD_SESSION) $(BUILD_DIR)/$(PROJECT).bin.sbin scp_packets $(TEST_KEY)
