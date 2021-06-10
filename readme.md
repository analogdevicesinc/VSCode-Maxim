# VSCode-Maxim

# Introduction
This is a [Visual Studio Code](https://code.visualstudio.com/)-based development environment for [Maxim Integrated's](https://www.maximintegrated.com/en/products/microcontrollers.html) microcontrollers.  It builds off of Microsoft's C/C++ extension and leverages Maxim's toolchain into a full-featured IDE for building and debugging embedded code.

Currently, **only Windows is supported**.  Support for MacOS and Linux toolchains is planned once Windows is stabilized.  MacOS has been tested and found to have some bugs.  Linux is untested.

# TODOs
* Troubleshoot Pause bug
* Add additional images to the readme.

# Requirements
* [Visual Studio Code](https://code.visualstudio.com/)
* [Maxim Micros SDK](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0010820A) (If you are using any of the micros below)
    * MAX32520
    * MAX32570
    * MAX32655
    * MAX32660
    * MAX32665-MAX32668
    * MAX32670
    * MAX32672
    * MAX32675
    * MAX78000
* [Maxim LP Micros SDK](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0001500A) (If you are using any of the micros below)
    * MAX3263x
    * MAX32600
    * MAX32620
    * MAX32625
    * MAX32650
* [C/C++ VSCode Extension](https://github.com/microsoft/vscode-cpptools) (This can be installed from within VSCode via the extension manager.  Search for `ms-vscode.cpptools`)
* The latest [Release](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) of this repository.


# Initial Setup/Installation
## Enabling Workspace Trust
The workspaces in this repo set environment variables for the integrated terminal.  In order for this to work, workspace trust must be enabled in your User Settings.  Follow the produre below.  You only need to do this one time per VS Code installation.

1. Launch VS Code.

2. Open your settings with `File > Preferences > Settings`.

3. Find the `security.workspace.trust` settings (you can paste it into the searchbar), and enable Workspace Trust with the checkbox, as shown below.  It's also a good idea to set the startup prompt to 'always'.

![Workspace Trust Settings Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/workspaceTrust.JPG)


4. Enable `terminal.integrated.allowWorkspaceConfiguration` with the checkbox, as shown below.

![Workspace Modification Setting Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/workspaceModification.JPG)

When opening workspaces and folders for the first time VSCode will now prompt for trust, as shown below.

![Workspace Trust Prompt Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/workspaceTrustPrompt.JPG)

The .JSON source files within the .vscode folders of this repo contain all of the modifications made by this workspace.  Mainly, a few directories are appended to the system Path variable used by the integrated terminal to make the toolchain accessible from the command line.

# Projects

## Project Creation
Projects can be created by:
* (Option 1) Starting with a pre-made example project.
* (Option 2) Injecting into an empty directory to create a new project.
* (Option 3) Injecting into a directory with existing source code.

**For the procedures below, you will pull content from the correct sub-folder for your SDK.  For the Maxim Micros SDK, use the contents of the `MaximSDK` folder.  For the LP Micros SDK, use the contents of the `MaximLP` folder.**

### Option 1 - Starting with a Pre-Made Project
Starting with the pre-made "Hello world" example is a great way to get rolling quickly.  Take this option if you would like to start with a (mostly) pre-configured project.

1. Copy the `New_Project` folder from the release package to an accessible location.  This will be the location of your project.  

2. (Optional) Rename the folder.  For example, I might rename the folder to `MyProject`.

3. Set your target microcontroller correctly.  See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller), and then return here.

4. That's it!  The "Hello World" project is ready to build, debug, and modify.  Some common next steps are:
    * [Testing the Setup](#Testing-the-Setup)
    * [Adding Source Files](#Adding-Source-Files)
    * [Building](#Building)
    * [Debugging](#Debugging)

### Option 2 - Creating a New Project
If you want to start from scratch, take this option.

1. Create your project folder.  For example, I might create a new project in a workspace folder with the path: `C:\Users\Jake.Carter\workspace\MyNewProject`.

2. Copy the **contents** of the `Inject` folder into the project folder created in step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyProject' folder would be the following :

        C:\Users\Jake.Carter\workspace\MyNewProject
        +-- \.vscode
        +-- Makefile

3. Set your target microcontroller correctly.  See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller), and then return here.

3. Fundamentally, that's it.  Your new empty project can now be opened with `File > Open Folder` from within VS Code.  However, you'll probably want to add some source code.  Common next steps are:
    * [Testing the Setup](#Testing-the-Setup)
    * [Adding Source Files](#Adding-Source-Files)
    * [Configuring the Makefile](#Configuring-the-Makefile)    

### Option 3 - Injecting into Existing Source Code
If you have existing source code that you'd like to import, take this option.

1. Navigate to the root folder of your existing project.  For example, this might be located at `C:\Users\Jake.Carter\workspace\MyExistingProject`.

2. Copy the contents of the `Inject` folder into the root of the project folder from step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyExistingProject' workspace might now look like the following :

        C:\Users\Jake.Carter\workspace\MyNewProject
        +-- /.vscode
        +-- Makefile
        +-- /src
            +-- main.c
            +-- mysource.c
        +-- /some_library
            +-- /src
                +-- theirsource.c
            +-- /include
                +-- theirheader.h
    
    Here I've injected the environment into a project where the source code has been organized into a `src` folder.  There is also another sub folder `some_library` that contains the source code to some other library that's part of my project.

3. Modify the Makefile to build your existing source code as necessary.  See [Configuring the Makefile](#Configuring-the-Makefile).  In the example above, I would add the following lines to the Makefile:

        SRCS += mysource.c
        SRCS += theirsource.c
        VPATH += ./some_library/src
        IPATH += ./some_library/include

4. With the Makefile configured for your existing source code, you'll also want to [set your target microcontroller](#Changing-the-Target-Microcontroller) correctly.

5. That's it!  The project is now configured around your existing source code.  Some common next steps are:
    * [Testing the Setup](#Testing-the-Setup)
    * [Building](#Building)
    * [Debugging](#Debugging)

## Testing the Setup
After creating and configuring your project, the toolchain should be accessible from the integrated terminal.  To test that everything is working properly : 

* Navigate to the open `TERMINAL` tab on the bottom of the VS Code application.  If a terminal is not open, you can open a new terminal with `Terminal > New Terminal` or (Ctrl+Shift+`).  The following commands to retrieve version numbers should be able to be run successfully from within the terminal :

    * `make -v`
    * `openocd -v`
    * `arm-none-eabi-gcc -v`
    * `arm-none-eabi-gdb -v`


# Building
There are 4 available build tasks that can be accessed via `Terminal > Run Build task...` or the shortcut `Ctrl+Shift+B`.
* Build
    * Compiles the code via the `make all` command.
    * The `./build` directory will be created and will contain the output binary, as well as all intermediary object files.
    * Any compiler errors/warnings will be output to the terminal during the build.
    * Make sure the target microcontroller is set correctly.  See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller).

* Clean
    * This task cleans the build output via the `make clean` command, removing the `./build` directory and all of its contents.

* Clean-Periph
    * This task is the same as 'clean', but it also removes the build output for Maxim's peripheral drivers.  
    * Use this if you would like to recompile the peripheral drivers on the next build.  
    * **This option is only present in the MaximSDK environment**

* Flash
    * This task runs the Build task, and then flashes the output binary to the microcontroller.
    * A programmer/debugger must be connected to the target microcontroller and host PC.
    * After flashing, the reset button on the microcontroller must be pushed or the micro must be power cycled to start execution of the program.

# Debugging
The Debugger can be launched with `Run > Start Debugging`, with the shortcut `F5`, or via the `Run and Debug` window (Ctrl + Shift + D).  All standard debugging features are supported - breakpoints, watch variables, etc.  However, there is a known bug with pausing.  At this time, pausing code execution will cause VSCode to throw an error.  Breakpoints should be used as an alternative.
* Ensure that a debugger/programmer is attached to the microcontroller and the host PC before launching a debugging session.
* When a debugging session is launched, the Build task will be launched automatically.  A successful build must be completed before debugging.

## Changing the Debug Adapter
Projects are configured to use the MAX32625PICO debug adapter by default.  **Only the PICO debug adapter has been thoroughly tested at this time.**  To use a different debugger:

1. Open the `.vscode/settings.json` file.

2. Change the `"debugger"` variable.  Options are:

    * "cmsis-dap" (for default PICO adapter)
    * "olimex-arm-usb-ocd" (for http://www.olimex.com/dev/arm-usb-ocd.html)
    * "olimex-arm-usb-ocd-h" (for http://www.olimex.com/dev/arm-usb-ocd.html)
    * "olimex-arm-usb-tiny-h" (for http://www.olimex.com/dev/arm-usb-tiny-h.html)
    * "olimex-jtag-tiny" (for http://www.olimex.com/dev/arm-usb-tiny.html)
    * "ftdi/olimex-arm-jtag-swd" (for https://www.olimex.com/Products/ARM/JTAG/ARM-JTAG-SWD/ w/ ftdi interface)
    * "ftdi/olimex-arm-usb-ocd" (for http://www.olimex.com/dev/arm-usb-ocd.html w/ ftdi interface)
    * "ftdi/olimex-arm-usb-ocd-h" (for http://www.olimex.com/dev/arm-usb-ocd-h.html w/ ftdi interface)
    * "ftdi/olimex-arm-usb-tiny-h" (for http://www.olimex.com/dev/arm-usb-tiny-h.html w/ ftdi interface)
    * "ftdi/olimex-jtag-tiny" (for http://www.olimex.com/dev/arm-usb-tiny.html w/ ftdi interface)

# Advanced Configuration

## Changing the Target Microcontroller
The default target microcontrollers are the MAX32655 (for the Maxim SDK) and the MAX32665 (for the LP SDK).  If you are using a different microcontroller, the target setting must be changed.  Follow the procedure below:

1. Open the `.vscode/settings.json` file.

2. Change the `"target"` variable to the correct value for your microcontroller.

Options for the Maxim Micros SDK are:
* "MAX32520"
* "MAX32570"
* "MAX32655"
* "MAX32660"
* "MAX32665" (for MAX32665-MAX32668)
* "MAX32670"
* "MAX32672"
* "MAX32675"
* "MAX78000"

Options for the LP Micros SDK are:
* "MAX3263x"
* "MAX32600"
* "MAX32620"
* "MAX32625"
* "MAX32650"

## Configuring the Makefile
The Makefile is the core file for the build system.  All configuration tasks such as adding source files to the build, setting compiler flags, and linking libraries are handled via the Makefile. The [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html) is a good one to have on hand.

### Adding Source Files
* The Makefile is pre-configured for a single `main.c` source file by default.  Add/edit additional source files to the build with additional `SRCS += yourfile.c`
* The Makefile looks for source files _only_ in the `\src` directory by default.  If you would like to use additional source directories, add them with `VPATH += yoursourcedirectory`
* The Makefile looks for header files _only_ in the `\src` directory by default.  If you would like to use additional include directories, add them with `IPATH += yourincludedirectory`

### Compiler Flags
* Compiler flags can be added/changed via the `PROJ_CFLAGS` variable.
* Add a new flag to be passed to the compiler with `PROJ_CFLAGS += -yourflag`.  Flags are passed in the order that they are added to the `PROJ_CFLAGS` variable.

### Linking Libraries
* Additional libraries can be linked via the `PROJ_LIBS` variable.  Add a new library to the build with `PROJ_LIBS += yourlibraryname`.
    * Note : Do not include the 'lib' part of the library name, or the file extension.  For example, to link `libarm_cortexM4lf_math.a` set `PROJ_LIBS += arm_cortexM4lf_math`.
* Tell the linker where to find the library with the '-L' linker flag.  Set `PROJ_LDFLAGS += -Lpathtoyourlibrary`.  For example, set `PROJ_LDFLAGS += -L./lib` to search a 'lib' directory inside of the project for libraries. 

### Optimization Level
* The optimization level that the compiler uses can be set by changing the `MXC_OPTIMIZE_CFLAGS` variable.  See [GCC Optimization Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) for more details on available optimization levels.  For example, disable optimization with `MXC_OPTIMIZE_CFLAGS = -O0`

## Setting Include Paths for Intellisense
VS Code's intellisense engine must be told where to find the header files for your source code.  By default, include paths have been added for Maxim's perpiheral drivers, and all of the sub-directories of the workspace will be searched for header files.  If VS Code throws an error on an `#include` statement (and the file exists), then an include path is most likely missing.

To add additional include paths :
1. Open the `.vscode/c_cpp_properties.json` file.  

2. Add the include path(s) to the `configurations > includePath` list.

## Using with a Non-Default SDK Installation Location
If you have installed Maxim's SDK to a non-default installation location, the `MAXIM_PATH` variable must be set accordingly.  To do so:

1. Open the `.vscode/settings.json` file.

2. Set the `MAXIM_PATH` to the root directory of your toolchain installation.  Use `/` (forward slashes) for the path.

# Known Issues
## 'An Exception Occurred' on Main
There is a known issue when debugging where a false exception is thrown on main when the debugger is started.  A temporary workaround can be used to get rid of this false exception message - set a breakpoint on main.

This issue does not affect the functionality of the debugger.

## Pausing Code Exection throws an Error
This is a known issue, and we believe this is related to how the .cpptools extension is sending messages to the core MIEngine.  Investigation is underway.
