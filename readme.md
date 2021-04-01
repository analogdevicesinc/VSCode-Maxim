# VSCode-Maxim
## Introduction
This is a [Visual Studio Code](https://code.visualstudio.com/)-based development environment for [Maxim Integrated's](https://www.maximintegrated.com/en/products/microcontrollers.html) microcontrollers.  It builds off of Microsoft's excellent C/C++ extension and leverages Maxim's toolchain into a full-featured IDE for building and debugging embedded code.


## Requirements
Before getting started, ensure that you have installed all of the dependencies below :
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
* [C/C++ VSCode Extension](https://github.com/microsoft/vscode-cpptools) (This can be installed from within VSCode via the extension manager.  Search for ms-vscode.cpptools)


## Setup
This VS Code environment can be injected into any workspace by copying the correct `.vscode` folder and `Makefile` into the root directory of the workspace.  You can create a new project from scratch by injecting into an empty directory (Option 1), or inject into a project with existing source code (Option 2)

### Option 1 - Creating an Empty Workspace
1. Download the correct injection package from [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) for your SDK.

2. Create your workspace folder.  For example, I might create a workspace for a new project with the path `C:\Users\Jake.Carter\workspace\MyNewProject`.

3. Copy the contents of the release package downloaded in step 1 into the workspace folder created in step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyProject' workspace would be the following :

        C:\Users\Jake.Carter\workspace\MyNewProject
        +-- \.vscode
        +-- Makefile

4. Start Visual Studio Code.

5. `File > Open Folder`

6. Browse to the root directory of the workspace folder created in step 2.

7. From within VS Code, open the `settings.json` file located in the `.vscode` folder.

8. Set the `target` variable to the correct microcontroller you are using.

9. That's it!  See [Testing the Setup](<#Testing the Setup>) below to verify everything is working properly, [Usage](#Usage) for using the VS Code environment, and [Makefile Configuration](<#Makefile Configuration>) for details on adding source code to the project.

### Option 2 - Injecting into an Existing Project
1. Download the correct injection package from [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) for your SDK.

2. Navigate to the root folder of your existing project.  For example, this might be located at `C:\Users\Jake.Carter\workspace\MyExistingProject`.

3. Copy the contents of the release package downloaded in step 1 into the root of the workspace folder from step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyExistingProject' workspace might look like the following :

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

8. Set the `target` variable to the correct microcontroller you are using.

9. The VS Code environment is now injected, but you will need to do some additional configuration of the Makefile to add in your existing source code to the build process.  See [Makefile Configuration](<#Makefile Configuration>) for details on how to do this, [Testing the Setup](<#Testing the Setup>) below for verifying everything is working properly, and [Usage](#Usage) for using the VS Code environment.  

### Testing the Setup
After injecting with Option 1 or Option 2, your toolchain should be accessible from the terminal.  To test that everything is working properly : 

* Navigate to the open `TERMINAL` tab on the bottom of the VS Code application.  If a terminal is not open, you can open a new terminal with `Terminal > New Terminal` or (Ctrl+Shift+`).  You should be able to run the following commands to retrieve version numbers successfully from within the terminal :

    * `make -v`
    * `openocd -v`
    * `arm-none-eabi-gcc -v`
    * `arm-none-eabi-gdb -v`


## Usage
### Building
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

### Debugging
The Debugger can be launched with `Run > Start Debugging`, with the shortcut `F5`, or via the `Run and Debug` window (Ctrl + Shift + D).  All standard debugging features are supported - breakpoints, watch variables, pausing, etc.
* Ensure that a debugger/programmer is attached to the microcontroller and the host PC before launching a debugging session.
* When a debugging session is launched, the Build task will be launched automatically.  A successful build must be completed before debugging.


## Makefile Configuration
The Makefile is the core file for the build system.  All configuration tasks such as adding source files to the build, setting compiler flags, and linking libraries are handled via the Makefile. The [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html) is a good one to have on hand.

### Adding Source Files
* The Makefile is pre-configured for a single `main.c` source file.  Add/edit additional source files for your project with additional `SRCS += yourfile.c`
* The Makefile looks for source files _only_ in the `\src` directory.  If you would like to use additional source directories, add them with `VPATH += yoursourcedirectory`
* The Makefile looks for header files _only_ in the `\src` directory.  If you would like to use additional include directories, add them with `IPATH += yourincludedirectory`

### Configuring Include Paths for Intellisense
* VS Code needs all include paths to be specified in order for the Intellisense engine to work properly.
* Include paths for intellisense are added via the `.vscode > c_cpp_properties.json` file.  Additional entries can be made in the `configurations > includePath` list.  The `\src` directory and include paths for Maxim's peripheral drivers are set up by default.

### Compiler Flags
* Compiler flags can be added/changed via the `PROJ_CFLAGS` variable.
* Add a new flag to be passed to the compiler with `PROJ_CFLAGS += -yourflag`.  Flags are passed in the order that they are added to the `PROJ_CFLAGS` variable.

### Linking Libraries
* Additional libraries can be linked via the `PROJ_LIBS` variable.  Add a new library to the build with `PROJ_LIBS += yourlibraryname`.
    * Note : Do not include the 'lib' part of the library name, or the file extension.  For example, to link `libarm_cortexM4lf_math.a` set `PROJ_LIBS += arm_cortexM4lf_math`.
* Tell the linker where to find the library with the '-L' linker flag.  Set `PROJ_LDFLAGS += -Lpathtoyourlibrary`.  For example, set `PROJ_LDFLAGS += -L./lib` to search a 'lib' directory in the workspace for libraries. 

### Optimization Level
* The optimization level that the compiler uses can be set by changing the `MXC_OPTIMIZE_CFLAGS` variable.  See [GCC Optimization Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) for more details on available optimization levels.  For example, disable optimization with `MXC_OPTIMIZE_CFLAGS = -O0`