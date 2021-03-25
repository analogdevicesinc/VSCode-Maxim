# VSCode-Maxim
## Introduction
This is a [Visual Studio Code](https://code.visualstudio.com/)-based development environment for [Maxim Integrated's](https://www.maximintegrated.com/en/products/microcontrollers.html) microcontrollers.  It builds off of Microsoft's excellent C/C++ extension, and leverages Maxim's toolchain into a full-featured IDE for building and debugging embedded code.

Some advanced setup is necessary, so a working knowledge of build systems (specifically GNU Make), include paths, command line interfaces, and environment variables is helpful but not required.

## Requirements
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

## Initial Setup
### Windows 10
The setup below involves making sure the necessary toolchain executables (compiler, linker, debugger, etc.) are accessible from the terminal, which involves creating a new system environment variable and setting entries in the Path variable.  

1. Ensure that you have met the above requirements.

2. Open the environment variables editor.  (`Control Panel > System and Security > System > Advanced System Settings > Environment Variables...`)

3. Add a new variable by clicking on the "New..." button for User variables.  Using the System variables will also work, provided you have administrative rights to do so.
    * For "Variable name" enter: `MAXIM_PATH`
    * For "Variable value" enter the installation directory for the SDK you installed above.
        * For the Maxim Micros SDK the default is `C:\MaximSDK`
        * For the Maxim LP Micros SDK the default is `C:\Maxim`
    * Hit OK to save the variable.
    
4. Edit your "Path" variable under User variables (or System variables if you have rights) and add the following entries, where ~ indicates the root installation directory of the SDK.  For example, `~\MaximSDK\Tools\MinGW\msys\1.0\bin` would be added as `C:\MaximSDK\Tools\MinGW\msys\1.0\bin` for a default installation located in the root directory of the C drive.
    * If you are using the Maxim Micros SDK add the following entries :
        * `~\MaximSDK\Tools\MinGW\msys\1.0\bin`
        * `~\MaximSDK\Tools\OpenOCD`
        * `~\MaximSDK\Tools\GNUTools\bin`
    * If you are using the Maxim LP Micros SDK add the following entries :
        * TODO
    * Hit OK to save the changes to the Path variable.

5. Hit OK to save these additions, and Apply/OK in the system properties window to push them to the system.

Your toolchain should now be accessible from the terminal.  To test that everything is working properly, start (or restart) VS Code and open a new terminal (Ctrl+Shift+`).  You should be able to run the following commands to retrieve version numbers successfully :
* `make -v`
* `openocd -v`
* `arm-none-eabi-gcc -v`
* `arm-none-eabi-gdb -v`

## Project Setup
The VS Code environment can be injected into a project with existing source code, or used as the basis for a new project to build up from scratch.

### Injection
A VS Code environment can be injected into an existing project by copying the contents of the correct folder from this repository into the root directory of the existing project.  To inject the environment :

1. Clone this repository to an accesible location.

2. Copy the _contents_ of the correct folder into the root directory of your project.
    * For the Maxim Micros SDK, use the contents of the "MaximSDK" folder.
    * For the Maxim LP Micros SDK, use the contents of the "MaximLP" folder.

3. Open VS Code, and open the root directory of your project with `File > Open Folder...` From this point on, this root directory folder will be referred to as your _workspace folder_.

4. Click on the Makefile to open it in the editor.

5. Change `PROJECT=changeme!` to set the `PROJECT` variable equal to the folder name of your workspace.  
    * For example, I've just injected a VS Code environment into my workspace at `C:\Users\Jake.Carter\Projects\MyProject`. I would set `PROJECT=MyProject`.
    * This is necessary for the debugger and flasher to work.  VS Code is set up to look for compiled binaries at the exact location `build\[WORKSPACE FOLDER NAME].elf`, so we need to configure the Makefile to name its output binaries correctly.  Think of the name of your workspace folder as the name of your project.  

### Makefile Configuration
The Makefile is the core file for the build system.  All configuration tasks such as adding source files to the build, setting compiler flags, and linking libraries are handled via the Makefile. The [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html) is a good one to have on hand.

#### Adding Source Files
* The Makefile is pre-configured for a single `main.c` source file.  Add/edit additional source files for your project with additional `SRCS += yourfile.c`
* The Makefile looks for source files _only_ in the `/src` directory.  If you would like to use additional source directories, add them with `VPATH += yoursourcedirectory`
* The Makefile looks for header files _only_ in the `/src` directory.  If you would like to use additional include directories, add them with `IPATH += yourincludedirectory`

#### Configuring Include Paths for Intellisense
* VS Code needs all include paths to be specified in order for the Intellisense engine to work properly.
* Include paths for intellisense are added via the `.vscode > c_cpp_properties.json` file.  Additional entries can be made in the `configurations > includePath` list.  The `/src` directory and include paths for Maxim's peripheral drivers are set up by default.

#### Compiler Flags
* Compiler flags can be added/changed via the `PROJ_CFLAGS` variable.
* Add a new flag to be passed to the compiler with `PROJ_CFLAGS += -yourflag`.  Flags are passed in the order that they are added to the `PROJ_CFLAGS` variable.

#### Linking Libraries
* Additional libraries can be linked via the `PROJ_LIBS` variable.  Add a new library to the build with `PROJ_LIBS += yourlibraryname`.
    * Note : Do not include the 'lib' part of the library name, or the file extension.  For example, to link `libarm_cortexM4lf_math.a` set `PROJ_LIBS += arm_cortexM4lf_math`.
* Tell the linker where to find the library with the '-L' linker flag.  Set `PROJ_LDFLAGS += -Lpathtoyourlibrary`.  For example, set `PROJ_LDFLAGS += -L./lib` to search a 'lib' directory in the workspace for libraries. 

#### Optimization Level
* The optimization level that the compiler uses can be set by changing the `MXC_OPTIMIZE_CFLAGS` variable.  See [GCC Optimization Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) for more details on available optimization levels.  For example, disable optimization with `MXC_OPTIMIZE_CFLAGS = -O0`

## Usage
### Building
There are 4 available build tasks that can be accessed via `Terminal > Run Build task...` or the shortcut `Ctrl+Shift+B`.
* Build - Compiles the code.  
    * You will be prompted for a target microcontroller for the build.  The `/build` directory will be created and will contain the output binary, as well as all intermediary object files.
    * Any compiler errors/warnings will be output to the terminal during the build.
* Clean - This cleans the build output and removes the `/build` directory and all of its contents.
* Clean-hard - The same as 'clean', but it also removes the build output for Maxim's peripheral drivers.  Use this if you would like to recompile the peripheral drivers on the next build.
* Flash - Flashes the program binary to the target microcontroller.
    * A successful build must be run to compile the program binaries before calling this task.
    * Additionally, a PICO programmer must be connected to the target microcontroller.

### Debugging
The Debugger 