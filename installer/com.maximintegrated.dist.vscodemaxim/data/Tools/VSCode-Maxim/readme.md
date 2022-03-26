# VSCode-Maxim
https://github.com/MaximIntegratedTechSupport/VSCode-Maxim

If you are viewing this document from within Visual Studio Code, press `CTRL+SHIFT+V` to open a Markdown preview window.

# Introduction
This repository is dedicated to maintaining [Visual Studio Code](https://code.visualstudio.com/) project files that integrate with [Maxim Integrated's](https://www.maximintegrated.com/en/products/microcontrollers.html) Microcontroller SDK.  The following features are enabled by the project files:
* Code editing with intellisense and definition look-ups down to the register level
* Code compilation with the ability to easily re-target a project for different microcontrollers and boards
* Flashing program binaries
* GUI and command-line debugging

# Dependencies
The project folders in this repo have the following dependencies:
* [Visual Studio Code](https://code.visualstudio.com/)
* [C/C++ VSCode Extension](https://github.com/microsoft/vscode-cpptools)
* [Maxim Micros SDK](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0010820A)

# Installation
## Windows 10
1. Download & install the Maxim Microcontrollers SDK via the [Windows Installer](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0010820A).  See [AN7219](https://www.maximintegrated.com/en/design/technical-documents/userguides-and-manuals/7/7219.html) for a detailed installation guide if needed.  (If the SDK is already installed, run the "MaintenanceTool.exe" to update it to the latest version)

    **Ensure all components are selected!**

    ![All components selected](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/installer_components.JPG)

2. Set the `MAXIM_PATH` environment variable to the installation location of the SDK.  If you are unsure how to set an environment variable, see [this](https://www.onmsft.com/how-to/how-to-set-an-environment-variable-in-windows-10) article.  Ex:

    ![Variable Name = MAXIM_PATH, Variable Value = C:/MaximSDK](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/maxim_path_env.JPG)

3. Download the latest Windows 10 release of this project from the [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) page and extract to an accessible location.

4. Copy the files from the `MaximSDK` folder into the root directory of your MaximSDK installation and overwrite.  This will populate the example projects with VS Code project folders and make any necessary patches to the SDK.

    ![Drag and Drop Installation](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/drag_and_drop_install.jpg)

5. Download & install [Visual Studio Code](https://code.visualstudio.com/).

6. Install official Microsoft [C/C++ VSCode Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools).

7. (Recommended) Disable VS Code auto updates in `File -> Preferences -> Settings` by setting `update.mode` to manual and `extensions.autoUpdate` to None.  VS Code updates on a monthly basis, and sometimes an auto-update can break the project files.  Additionally, feature changes on the vscode-cpptools extension may cause instability.  Tested version #s can be found on each Release page.

8. That's it!  You're ready to start using Visual Studio Code to develop with Maxim's Microcontrollers.  See Usage below.

## Linux
### Ubuntu
1. Download & install the Maxim Microcontrollers SDK via the [Linux Installer](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0018720A).  See [AN7219](https://www.maximintegrated.com/en/design/technical-documents/userguides-and-manuals/7/7219.html) for a detailed installation guide if needed.  (If the SDK is already installed, run the "MaintenanceTool" to update it to the latest version)

    **Ensure all components are selected!**

    ![All components selected](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/installer_components.JPG)

2. Add MAXIM_PATH to your system environment variables.
    1. Create a new file `/etc/profile.d/maximsdk-env.sh` with the contents `export MAXIM_PATH=[MaximSDK installation location]`.  
    
        For example...

        ```bash
        # in /etc/profile.d/maximsdk-env.sh ...
        export MAXIM_PATH=/home/yourusername/MaximSDK
        ```

        ... and save the file.

    2. Reboot your system to refresh environment variables system-wide.

3. Download the latest Linux release of this project from the [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) page and extract to an accessible location.

4. Copy the `60-openocd.rules` file from the VSCode-Maxim release into `/etc/udev/rules.d/` and refresh udev rules.  The following terminal commands can be used from within the VSCode-Maxim release folder...

    ```bash
    cp 60-openocd.rules /etc/udev/rules.d/
    udevadm control --reload 
    ```

5. Copy the files from the `MaximSDK` folder into the root directory of your MaximSDK installation and overwrite.  This will populate the example projects with VS Code project folders and make any necessary patches to the SDK.

    ![Drag and Drop Installation](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/drag_and_drop_install.jpg)
    (Note:  The image above shows a Windows file explorer...  The principal is the same on any OS)

6. Download & install [Visual Studio Code](https://code.visualstudio.com/).

7. Install official Microsoft [C/C++ VSCode Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools).

8. (Recommended) Disable VS Code auto updates in `File -> Preferences -> Settings` by setting `update.mode` to manual and `extensions.autoUpdate` to None.  VS Code updates on a monthly basis, and sometimes an auto-update can break the project files.  Additionally, feature changes on the vscode-cpptools extension may cause instability.  Tested version #s can be found on each Release page.

9. That's it!  You're ready to start using Visual Studio Code to develop with Maxim's Microcontrollers.  See Usage below.

# Usage
## Introduction
This section covers basic usage of the VSCode-Maxim project files.  For documentation on Visual Studio Code itself, please refer to the official docs [here](https://code.visualstudio.com/Docs).  

Prior experience with Visual Studio Code is not required to understand this section or use the project files, but some basic familiarity is helpful.  For new users, this initial familiarity can be gained by working through the full [User Guide](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/userguide.md).

## Opening Projects
Visual Studio Code is built around a "working directory" paradigm.  VS Code's editor is always running from inside of a working directory, and the main mechanism for changing that directory is `File -> Open Folder...`  

![File -> Open Folder](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/file_openfolder.JPG)

VS Code will look in the opened folder for a `.vscode` _sub_-folder to load project-specific settings from.

Opening an existing project is as simple as `File -> Open Folder...`.  A project that is configured for VS Code will have, at minimum, a .vscode sub-folder and a Makefile in its directory.  Ex:

![Example Directory Contents](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/opening_projects_2.jpg)

Note:  You may need to enable viewing of hidden items in your file explorer to see the .vscode sub-folder.

## Build Tasks
Once a project is opened 4 available build tasks will become available via `Terminal > Run Build task...` or the shortcut `Ctrl+Shift+B`.  These tasks are configured by the `.vscode/task.json` file.

![Build Tasks Image](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/buildtasks.JPG)

* Build
    * Compiles the code.
    * The `./build` directory will be created and will contain the output binary, as well as all intermediary object files.

* Clean
    * This task cleans the build output, removing the `./build` directory and all of its contents.
    
* Clean-Periph
    * This task is the same as 'clean', but it also removes the build output for Maxim's peripheral drivers.
    * Use this if you would like to recompile the peripheral drivers from source on the next build.

* Flash
    * This task runs the Build task, and then flashes the output binary to the microcontroller.
    * A debugger must be connected to the correct debugger port on the target microcontroller.  Refer to the datasheet of your microcontrollers evaluation board for instructions on connecting a debugger.

## Editing the Makefile
At the heart of every project is its `Makefile`.  Build Tasks are essentially a wrapper around the Makefile.  Adding source code files to the build, setting compiler flags, linking libraries, etc. must be done by directly editing this file.

The usage guidelines below are specific to Maxim's Makefiles.  The [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html) is a good one to have on hand for documentation regarding Makefiles in general.

### Adding Source Code Files
* VS Code's editor can create and add new files to a project, but they won't be added to the build automatically.  The Makefile must be told which source code files to build, and where to find them.
* Add a source file to the build with `SRCS += yourfile.c`
* The Makefile looks for project source files in the `/src` directory by default.  Add additional directories to search with `VPATH += yoursourcedirectory`
* The Makefile looks for project header files in the `/src` directory by default.  Add additional directories to search with `IPATH += yourincludedirectory`

### Compiler Flags
* Compiler flags can be added/changed via the `PROJ_CFLAGS` variable.
* Add a new flag to be passed to the compiler with `PROJ_CFLAGS += -yourflag`.  Flags are passed in the order that they are added to the `PROJ_CFLAGS` variable.

### Linking Libraries
* Additional libraries can be linked via the `PROJ_LIBS` variable.  Add a new library to the build with `PROJ_LIBS += yourlibraryname`.
    * Note : Do not include the 'lib' part of the library name, or the file extension.  For example, to link `libarm_cortexM4lf_math.a` set `PROJ_LIBS += arm_cortexM4lf_math`.
* Tell the linker where to find the library with the '-L' linker flag.  Set `PROJ_LDFLAGS += -Lpathtoyourlibrary`.  For example, set `PROJ_LDFLAGS += -L./lib` to search a 'lib' directory inside of the project for libraries. 

### Optimization Level
* The optimization level that the compiler uses can be set by changing the `MXC_OPTIMIZE_CFLAGS` variable.  
* See [GCC Optimization Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) for more details on available optimization levels.  For example, disable optimization with `MXC_OPTIMIZE_CFLAGS = -O0`

## Debugging
Debugging is enabled by Visual Studio Code's integrated debugger.  Launch configurations are provided by the `.vscode/launch.json` file.

![Debug Window](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/debugger.JPG)

### Launching the Debugger
1. Ensure that a debugger is attached to the target microcontroller on the correct port.  (Refer to the datasheet of your evaluation board for instructions on connecting a debugger)

2. Flash the program to the microcontroller with the "Flash" Build Task (CTRL+SHIFT+B).  Flashing does not happen automatically when launching the debugger.

3. Launch the debugger with `Run > Start Debugging`, with the shortcut `F5`, or via the `Run and Debug` window (Ctrl + Shift + D) and the green "launch" arrow.

    ![Debug Tab](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/debugger_window.JPG)

4. The debugger will launch a GDB client & OpenOCD server, reset the microcontroller, and should break on entry into `main`.

    ![Debugger Break on Main](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/debugger_breakmain.JPG)

### Using the Debugger
The main interface for the debugger is the debugger control bar.

![Debugger Control Bar Image](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/debugger_bar.JPG)

Continue | Step Over | Step Into | Step Out | Restart | Stop

Breakpoints can be set by clicking in the space next to the line number in a source code file.  A red dot indicates a line to break on.  Breakpoints can be removed by clicking on them again.  Ex:

![Breakpoint](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/breakpoint.JPG)

For full usage details, please refer to the [official VS Code debugger documentation](https://code.visualstudio.com/docs/editor/debugging).  Documentation related to launch configurations can be ignored, as that's what's provided by this project.

# Configuration
## Project Settings
`.vscode/settings.json` is the main project configuration file.  Values set here are parsed into the other .json config files.  When a change is made to this file, VS Code should be restarted (or alternatively reloaded with CTRL+SHIFT+P -> Reload Window) to force a re-parse.  

The default project configuration should work for most use cases as long as `"target"` and `"board"` are set correctly.

Any field from `settings.json` can be referenced from any other config file (including itself) with `"${config:[fieldname]}"`

The following configuration options are available:
## Basic Config Options
* `"target"`
    * This sets the target microcontroller for the project.
    * Supported values:
        * `"MAX32520"`
        * `"MAX32570"`
        * `"MAX32650"`
        * `"MAX32655"`
        * `"MAX32660"`
        * `"MAX32665"` (for MAX32665-MAX32668)
        * `"MAX32670"`
        * `"MAX32672"`
        * `"MAX32675"`
        * `"MAX78000"`
    
* `"board"`
    * This sets the target board for the project (ie. Evaluation Kit, Feather board, etc.)
    * Supported values: 
        * ... can be found in the `Libraries/Boards` folder of the MaximSDK
    * For example, the supported options for the MAX78000 are `"EvKit_V1"`, `"FTHR_RevA"`, and `"MAXREFDES178"`.
![MAX78000 Boards](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/78000_boards.JPG)

## Advanced Config Options
* `"terminal.integrated.env.[platform]:Path"`
    * This prepends the location of toolchain binaries to the system `Path` used by VSCode's integrated terminal.  Don't touch unless you know what you're doing :)

* `"MAXIM_PATH"`
    * This option must point to the root installation directory of the MaximSDK.  By default, the MAXIM_PATH environment variable is used, which is suitable for most use cases.  
    * Default value: `"${env:MAXIM_PATH}"`

* `"project_name"`
    * Sets the name of project.  This is used in other config options such as `program_file`.
    * Default value: `"${workspaceFolderBasename}"`

* `"program_file"`
    * Sets the name of the file to flash and debug.  This is provided in case it's needed, but for most use cases should be left at its default.  
    * File extension must be included.
    * Default value: `"${config:project_name}.elf"`

* `"symbol_file"`
    * Sets the name of the file that GDB will load debug symbols from.
    * File extension must be included.
    * Default value: `"${config:program_file}"`

* `"M4_OCD_interface_file"`
    * Sets the OpenOCD interface file to use to connect to the Arm M4 core.  This should match the debugger being used for the M4 core.
    * `.cfg` file extension must be included.
    * Default value: `"cmsis-dap.cfg"`

* `"M4_OCD_target_file"`
    * Sets the OpenOCD target file to use for the Arm M4 core.  This should match the target microcontroller.
    * `.cfg` file extension must be included.
    * **On Linux there is a case-sensitivity issue with this setting**.  OpenOCD config files are all lowercase, but `"target"` must be uppercase.  On Linux, manually set this value to the lowercase target .cfg file matching the `"target"` config option.  Ex:  `""M4_OCD_target_file":"max32670.cfg"`
    * Default value: `"${config:target}.cfg"`

* `"RV_OCD_interface_file"`
    * Sets the OpenOCD interface file to use to connect to the RISC-V core.  This should match the debugger being used for the RISC-V core.
    * `.cfg` file extension must be included.
    * Default value: `"cmsis-dap.cfg"`

* `"RV_OCD_target_file"`
    * Sets the OpenOCD target file to use for the RISC-V core.
    * `.cfg` file extension must be included.
    * Default value: `"${config:target}_riscv.cfg"`

* `"GCC_version"`
    * Sets the version of the Arm Embedded GCC to use, including toolchain binaries and the standard library version.

* `"v_xPack_GCC"`
    * Sets the version of the xPack RISC-V GCC to use.

* `"OCD_path"`
    * Where to find the OpenOCD.
    * Default value: `"${config:MAXIM_PATH}/Tools/OpenOCD"`

* `"ARM_GCC_path"`
    * Where to find the Arm Embedded GCC Toolchain.
    * Default value: `"${config:MAXIM_PATH}/Tools/GNUTools/gcc-arm-none-eabi-${config:GCC_version}"`

* `"RV_GCC_path"`
    * Where to find the RISC-V GCC Toolchain.
    * Default value: `${config:MAXIM_PATH}/Tools/xPacks/riscv-none-embed-gcc/${config:v_xPack_GCC}`

* `"Make_path"`
    * Where to find Make binaries (only used on Windows)
    * Default value: `"${config:MAXIM_PATH}/Tools/MinGW/msys/1.0/bin"`

## Setting Search Paths for Intellisense
VS Code's intellisense engine must be told where to find the header files for your source code.  By default, Maxim's perpiheral drivers, the C standard libraries, and all of the sub-directories of the workspace will be searched for header files to use with Intellisense.  If VS Code throws an error on an `#include` statement (and the file exists), then a search path is most likely missing.

To add additional search paths :
1. Open the `.vscode/c_cpp_properties.json` file.  

2. Add the include path(s) to the `configurations > includePath` list.  The paths set here should contain header files, and will be searched by the Intellisense engine and when using "Go to Declaration" in the editor.

3. Add the path(s) to any relevant implementation files to the `"browse":"path"` list.  This list contains the paths that will be searched when using "Go to Definition".  

# Project Creation
### Option 1.  Copying a Pre-Made Project
Copying a pre-made example project is a great way to get rolling quickly, and is currently the recommended method for creating new projects.  

The release package for this project contains a `New_Project` folder designed for such purposes.  Additionally, any of the VS Code-enabled Example projects can be copied from the SDK.

1. Copy the existing project folder to an accessible location.  This will be the location of your new project.

2. (Optional) Rename the folder.  For example, I might rename the folder to `MyProject`.

3. Open the project in VS Code (`File -> Open Folder...`)

4. Set your target microcontroller and board correctly.  See [Basic Config Options](#basic-config-options)

5. `CTRL+SHIFT+P -> Reload Window` to re-parse the project settings.

6. That's it!  The existing project is ready to build, debug, and modify.

### Option 2 - Creating a Project from Scratch
If you want to start from scratch, take this option.

1. Create your project folder.  For example, I might create a new project in a workspace folder with the path: `C:\Users\Jake.Carter\workspace\MyNewProject`.

2. Copy the **contents** of the `Inject` folder into the project folder created in step 2.  This includes a `.vscode` folder and a `Makefile`.  In the example above, the contents of the 'MyProject' folder would be the following :

        C:\Users\Jake.Carter\workspace\MyNewProject
        +-- \.vscode
        +-- Makefile

3. Open the project in VS Code (`File -> Open Folder...`)

4. Set your target microcontroller correctly.  See [Basic Config Options](#basic-config-options).

5. `CTRL+SHIFT+P -> Reload Window` to re-parse the project settings.

6. Fundamentally, that's it.  Your new empty project can now be opened with `File > Open Folder` from within VS Code.  However, you'll probably want to add some source code.  See [Configuring the Makefile](#configuring-the-makefile).

# Troubleshooting
## Testing the Setup
Opening a VSCode-Maxim project with `File > Open Folder` should make Maxim's toolchain accessible from the integrated terminal.  To test that everything is working properly : 

1. Navigate to the open `TERMINAL` tab on the bottom of the VS Code application.  If a terminal is not open, you can open a new terminal with `Terminal > New Terminal` or (Ctrl+Shift+`).  

   ![Terminal image](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/Terminal.JPG)

2. The following commands to retrieve version numbers should be able to be run successfully from within the terminal :

    * `make -v`
    * `openocd -v`
    * `arm-none-eabi-gcc -v`
    * `arm-none-eabi-gdb -v`
    
   For example, the `make -v` command should similar to the following:
   
   ![Make -v example output](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/make_test.JPG)

If the tools are not accessible from the terminal, then the system settings and/or project settings must be examined further.  (Troubleshooting guide is in progress)
