# VSCode-Maxim

# Introduction
This is a [Visual Studio Code](https://code.visualstudio.com/)-based development environment for [Maxim Integrated's](https://www.maximintegrated.com/en/products/microcontrollers.html) microcontrollers.  It builds off of Microsoft's excellent C/C++ extension and leverages Maxim's toolchain into a full-featured IDE for building and debugging embedded code.


# Requirements
**Before getting started, ensure that you have installed all of the dependencies below** :
* [Visual Studio Code](https://code.visualstudio.com/)
* [Maxim Micros SDK](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0010820A) (If you are using any of the micros below)
    * MAX32520
    * MAX32570
    * MAX32655
    * MAX32670
    * MAX32675
    * MAX78000
* [Maxim LP Micros SDK](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0001500A) (If you are using any of the micros below)
    * MAX3263x
    * MAX32520
    * MAX32600
    * MAX32620
    * MAX32625
    * MAX32650
    * MAX32660
    * MAX32665-MAX32668
* [C/C++ VSCode Extension](https://github.com/microsoft/vscode-cpptools) (This can be installed from within VSCode via the extension manager.  Search for `ms-vscode.cpptools`)


# Setup
This VS Code workspace modifies environment variables of the integrated terminal.  **Before proceeding, please enable workspace trust and workspace modifications, and then restart VSCode.**  Open your settings with `File > Preferences > Settings`.

Workspace trust can be enabled with the `security.workspace.trust` settings, as shown below.

<section align="center">

![Workspace Trust Settings Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/workspaceTrust.JPG)

</section>

Additionally, workspace modifications must be enabled via the `terminal.integrated.allowWorkspaceConfiguration` setting, as shown below.

<section align="center">

![Workspace Modification Setting Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/workspaceModification.JPG)

</section>

When opening workspaces and folders for the first time VSCode will now prompt for trust, as shown below.  This can be enabled/disabled with the `security.workspace.trust.startupPrompt` settings option.

<section align="center">

![Workspace Trust Prompt Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/workspaceTrustPrompt.JPG)

</section>

The .JSON source files within the .vscode folders of this repo contain all of the modifications made by this workspace.  Mainly, a few directories are appended to the system Path variable used by the integrated terminal to make the toolchain accessible from the command line.

# Project Setup
Projects can be created by:
* (Option 1) Injecting the workspace into an empty directory to create a new project.
* (Option 2) Injecting the workspace into a directory with existing source code to integrate into an existing project.
* (Option 3) Starting with a pre-made example project.

## Option 1 - Creating a New Project
1. Download the latest correct version of this repo from the [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) page for your SDK and extract it to an accessible location.

2. Create your project folder.  For example, I might create a new project in a workspace folder with the path: `C:\Users\Jake.Carter\workspace\MyNewProject`.

3. Copy the contents of the `Inject` folder into the project folder created in step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyProject' folder would be the following :

        C:\Users\Jake.Carter\workspace\MyNewProject
        +-- \.vscode
        +-- Makefile

4. Start Visual Studio Code.

5. `File > Open Folder`

6. Browse to the root directory of the workspace folder created in step 2.

7. From within VS Code, open the `settings.json` file located in the `.vscode` folder.

8. Set the `"target"` variable to the correct microcontroller you are using.  See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller) for value strings.

9. (Optional) Set the `MAXIM_PATH` variable to to the root directory of your toolchain installation.  This is only necessary if you used a non-default installation location.

10. That's it!  See [Testing the Setup](#Testing-the-Setup) below to verify everything is working properly, [Usage](#Usage) for using the VS Code environment, and [Build System Configuration](#Build-System-Configuration) for deeper configuration options such as adding source files, configuring intellisense paths, etc.

## Option 2 - Injecting into an Existing Project
1. Download the latest correct version of this repo from the [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) page for your SDK and extract it to an accessible location.

2. Navigate to the root folder of your existing project.  For example, this might be located at `C:\Users\Jake.Carter\workspace\MyExistingProject`.

3. Copy the contents of the `Inject` folder into the root of the project folder from step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyExistingProject' workspace might now look like the following :

        C:\Users\Jake.Carter\workspace\MyNewProject
        +-- \.vscode
        +-- Makefile
        +-- \src
            +-- main.c
            +-- my_header.h
            +-- \some_sub_folder
                +-- some_more_source.c
    
    Here I've injected the environment into a project where the source code has been organized into a `src` folder.  There is also another sub folder with some more source code.

4. Start Visual Studio Code.

5. `File > Open Folder`

6. Browse to the root directory of the workspace folder located in step 2.

7. From within VS Code, open the `settings.json` file located in the `.vscode` folder.

8. Set the `"target"` variable to the correct microcontroller you are using. See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller) for value strings.

9. (Optional) Set the `MAXIM_PATH` variable to to the root directory of your toolchain installation.  This is only necessary if you used a non-default installation location.

10. The VS Code environment is now injected, but you will need to do some additional configuration of the Makefile to add in your existing source code to the build process.  See [Adding Source Files](#Adding-Source-Files) for more details on this.

11. See [Testing the Setup](#Testing-the-Setup) below to verify everything is working properly, [Usage](#Usage) for using the VS Code environment, and [Build System Configuration](#Build-System-Configuration) for deeper configuration options such as adding source files, configuring intellisense paths, etc.

## Option 3 - Starting with a Pre-Made Project
1. Download the latest correct version of this repo from the [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) page for your SDK and extract it to an accessible location.

2. Copy the `New_Project` folder to an accessible location.  This will be the location of your project.  Rename the folder if you'd like.

3. Start Visual Studio Code.

4. `File > Open Folder`

5. Browse to the root directory of the extracted framework project from step 2.

6. From within VS Code, open the `settings.json` file located in the `.vscode` folder.

7. Set the `"target"` variable to the correct microcontroller you are using. See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller) for value strings.

8. (Optional) Set the `MAXIM_PATH` variable to to the root directory of your toolchain installation.  This is only necessary if you used a non-default installation location.

9. That's it!  See [Testing the Setup](#Testing-the-Setup) below to verify everything is working properly, [Usage](#Usage) for using the VS Code environment, and [Build System Configuration](#Build-System-Configuration) for deeper configuration options such as adding source files, configuring intellisense paths, etc.

## Testing the Setup
After injecting with Option 1 or Option 2, your toolchain should be accessible from the terminal.  To test that everything is working properly : 

* Navigate to the open `TERMINAL` tab on the bottom of the VS Code application.  If a terminal is not open, you can open a new terminal with `Terminal > New Terminal` or (Ctrl+Shift+`).  The following commands to retrieve version numbers should be able to be run successfully from within the terminal :

    * `make -v`
    * `openocd -v`
    * `arm-none-eabi-gcc -v`
    * `arm-none-eabi-gdb -v`


# Usage

## Building
There are 4 available build tasks that can be accessed via `Terminal > Run Build task...` or the shortcut `Ctrl+Shift+B`.
* Build
    * Compiles the code.  
    * Code will be compiled for the target the microcontroller set in `.vscode\settings.json`.  **Make sure this is set correctly!**
    * The `\build` directory will be created and will contain the output binary, as well as all intermediary object files.
    * Any compiler errors/warnings will be output to the terminal during the build.

* Clean
    * This task cleans the build output, removing the `\build` directory and all of its contents.

* Clean-Periph
    * This task is the same as 'clean', but it also removes the build output for Maxim's peripheral drivers.  
    * Use this if you would like to recompile the peripheral drivers on the next build.  
    * **This option is only present in the MaximSDK environment**

* Flash
    * This task runs the Build task automatically, and then flashes the output binary to the microcontroller.
    * A programmer/debugger must be connected to the target microcontroller and host PC.
    * After flashing, the reset button on the microcontroller must be pushed or the micro must be power cycled to start execution of the program.

## Debugging
The Debugger can be launched with `Run > Start Debugging`, with the shortcut `F5`, or via the `Run and Debug` window (Ctrl + Shift + D).  All standard debugging features are supported - breakpoints, watch variables, pausing, etc.
* Ensure that a debugger/programmer is attached to the microcontroller and the host PC before launching a debugging session.
* When a debugging session is launched, the Build task will be launched automatically.  A successful build must be completed before debugging.


# Build System Configuration

## Configuring the Makefile
The Makefile is the core file for the build system.  All configuration tasks such as adding source files to the build, setting compiler flags, and linking libraries are handled via the Makefile. The [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html) is a good one to have on hand.

### Adding Source Files
* The Makefile is pre-configured for a single `main.c` source file.  Add/edit additional source files for your project with additional `SRCS += yourfile.c`
* The Makefile looks for source files _only_ in the `\src` directory.  If you would like to use additional source directories, add them with `VPATH += yoursourcedirectory`
* The Makefile looks for header files _only_ in the `\src` directory.  If you would like to use additional include directories, add them with `IPATH += yourincludedirectory`

### Compiler Flags
* Compiler flags can be added/changed via the `PROJ_CFLAGS` variable.
* Add a new flag to be passed to the compiler with `PROJ_CFLAGS += -yourflag`.  Flags are passed in the order that they are added to the `PROJ_CFLAGS` variable.

### Linking Libraries
* Additional libraries can be linked via the `PROJ_LIBS` variable.  Add a new library to the build with `PROJ_LIBS += yourlibraryname`.
    * Note : Do not include the 'lib' part of the library name, or the file extension.  For example, to link `libarm_cortexM4lf_math.a` set `PROJ_LIBS += arm_cortexM4lf_math`.
* Tell the linker where to find the library with the '-L' linker flag.  Set `PROJ_LDFLAGS += -Lpathtoyourlibrary`.  For example, set `PROJ_LDFLAGS += -L./lib` to search a 'lib' directory in the workspace for libraries. 

### Optimization Level
* The optimization level that the compiler uses can be set by changing the `MXC_OPTIMIZE_CFLAGS` variable.  See [GCC Optimization Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) for more details on available optimization levels.  For example, disable optimization with `MXC_OPTIMIZE_CFLAGS = -O0`

## Setting Include Paths for Intellisense
VS Code's intellisense engine must be told where to find the header files for your source code.  By default, include paths have been added for Maxim's perpiheral drivers, and all of the sub-directories of the workspace will be searched for header files.  If VS Code throws an error on an `#include` statement (and the file exists), then an include path is most likely missing.

To add additional include paths :
1. Open the `\.vscode\c_cpp_properties.json` file.  

2. Add the include path(s) to the `configurations > includePath` list.

## Changing the Target Microcontroller
1. Open the `\.vscode\settings.json` file.

2. Change the `"target"` variable to the correct value for your microcontroller.
Options for the LP Micros SDK are:
    * "MAX3263x"
    * "MAX32520"
    * "MAX32600"
    * "MAX32620"
    * "MAX32625"
    * "MAX32650"
    * "MAX32660"
    * "MAX32665" (for MAX32665-MAX32668)

and options for the Maxim Micros SDK are:
    * "MAX32520"
    * "MAX32570"
    * "MAX32655"
    * "MAX32670"
    * "MAX32675"
    * "MAX78000"

# Known Issues
## 'An Exception Occurred' on Main
There is a known issue when debugging where a false exception is thrown on main when the debugger is started.  A temporary workaround can be used to get rid of this false exception message - set a breakpoint on main.

This issue does not affect the functionality of the debugger.
