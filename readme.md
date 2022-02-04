# VSCode-Maxim
https://github.com/MaximIntegratedTechSupport/VSCode-Maxim 

# Introduction
This repo contains [Visual Studio Code](https://code.visualstudio.com/) project folders for [Maxim Integrated's](https://www.maximintegrated.com/en/products/microcontrollers.html) microcontroller Software Development Kits (SDKs).

**Note:** This repository now contains a full [User Guide](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/userguide.md).

# Dependencies
The project folders in this repo have the following dependencies:
* [Visual Studio Code](https://code.visualstudio.com/)
* [C/C++ VSCode Extension](https://github.com/microsoft/vscode-cpptools)
* [Maxim Micros SDK](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0010820A), which supports the following microcontrollers:
    * MAX32520
    * MAX32570
    * MAX32650
    * MAX32655
    * MAX32660
    * MAX32665-MAX32668
    * MAX32670
    * MAX32672
    * MAX32675
    * MAX32680
    * MAX32690
    * MAX78000
    * MAX78002

# Installation
## Windows
1. Download & install the Maxim Microcontrollers SDK via the [Windows Installer](https://www.maximintegrated.com/content/maximintegrated/en/design/software-description.html/swpart=SFW0010820A).  See [AN7219](https://www.maximintegrated.com/en/design/technical-documents/userguides-and-manuals/7/7219.html) for a detailed installation guide if needed.

2. Set the `MAXIM_PATH` environment variable to the installation location of the SDK.  If you are unsure how to set an environment variable, see [this](https://www.onmsft.com/how-to/how-to-set-an-environment-variable-in-windows-10) article.  Ex:

![Variable Name = MAXIM_PATH, Variable Value = C:/MaximSDK](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/maxim_path_env.JPG)

3. Download & install [Visual Studio Code](https://code.visualstudio.com/).

4. Install official Microsoft [C/C++ VSCode Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools).

5. (Recommended) Disable VS Code auto updates in `File -> Preferences -> Settings` by setting `update.mode` to manual.  VS Code updates on a monthly basis, and sometimes an auto-update can break the project files.

6. That's it!  You're ready to start using Visual Studio Code to develop with Maxim's Microcontrollers.  See Usage below.

## Linux
### Ubuntu
1. Download the latest Ubuntu release from the [Releases](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) page and extract to an accessible location.

2. Open a terminal in the extracted folder.  Run: 
    ```bash
    sudo -u [your username] bash install.sh
    ```

3. Follow the instructions in the installer and run the script to completion.

4. Run...
    ```bash
    bash setup.sh
    ```
    ... to populate the SDK with VS Code project files and complete the installation.

5. (Recommended) Disable VS Code auto updates in `File -> Preferences -> Settings` by setting `update.mode` to manual.  VS Code updates on a monthly basis, and sometimes an auto-update can break the project files.

6. That's it!  You're ready to start using Visual Studio Code to develop with Maxim's Microcontrollers.  See Usage below.

## Enabling Workspace Trust
In order for the project folders to function workspace trust must be enabled in your User Settings.  It should be by default.  Follow the procedure below to check/enable it.  You only need to do this one time per VS Code installation.

1. Launch VS Code.

2. Open your settings with `File > Preferences > Settings`.

3. Find the `security.workspace.trust` settings (you can copy+paste this into the searchbar), and enable Workspace Trust with the checkbox, as shown below.  It's also a good idea to set the startup prompt to 'always'.

![Workspace Trust Settings Image](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/workspaceTrust.JPG)

When opening workspaces and folders for the first time VSCode will now prompt for trust, as shown below.

![Workspace Trust Prompt Image](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/workspaceTrustPrompt.JPG)

The .JSON source files within the .vscode folders of this repo contain all of the modifications made by this workspace.  Mainly, a few directories are appended to the system Path variable used by the integrated terminal to make the toolchain accessible from the command line.

# Usage
Visual Studio Code is built around a "working directory" paradigm.  VS Code's editor is always running from inside of a working directory, and the main mechanism for changing that directory is `File > Open Folder`.  Once the folder is opened VS Code will look inside of it for a `.vscode` sub-folder to load project-specific settings from.  The project folders in this repository tell VS Code how to integrate with Maxim's SDK and toolchain, and allows for code editing with working peripheral driver function lookups as well as debugging.

As such, a VSCode-Maxim project contains two main components:  A `.vscode` folder and a `Makefile`.  
* The .vscode folder contains .json files that tell Visual Studio Code how to use Maxim's Makefiles.  It also tells VS Code how to use Maxim's toolchain to flash and debug the project on a target microcontroller.
* The Makefile describes how to use Maxim's toolchain to build a project's source code.

The main mechanism for creating a new project is copying the `.vscode` folder and Makefile ("injecting" it) into another "receiver" folder.  If the receiver folder is empty, then the new project is ready for `File > Open Folder`.  Otherwise, if it contains existing source code and/or an existing Makefile, the new project will require some minimal setup.  A quick-start guide for both scenarios is provided below, and a detailed walkthrough can also be found in the [User Guide](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/userguide.md).

# Configuration
## Project Settings
`.vscode/settings.json` is the main project configuration file.  Values set here are parsed into the other .json config files.  When a change is made to this file, VS Code should be restarted (or alternatively reloaded with CTRL+SHIFT+P -> Reload Window) to force a re-parse.  

The default project configuration should work for most use cases as long as `"target"` and `"board"` are set correctly.

The following configuration options are available:
## Common Config Options
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
    * The available options will depend on your target microcontroller, and can be found in the `Libraries/Boards` folder of the MaximSDK
    * For example, the supported options for the MAX78000 are `"EvKit_V1"`, `"FTHR_RevA"`, and `"MAXREFDES178"`.
![MAX78000 Boards](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/78000_boards.JPG)

## Advanced Config Options
* `"terminal.integrated.env.[platform]:Path"`
    * This prepends the location of toolchain binaries to the system `Path` used by VSCode's integrated terminal.  Don't touch unless you know what you're doing :)

* `"MAXIM_PATH"`
    * This option must point to the root installation directory of the MaximSDK.  
    * Default value: `"${env:MAXIM_PATH}"`, which loads the MAXIM_PATH environment variable set in the installation process.

* `"project_name"`
    * Sets the name of project.  This is used in other config options such as `program_file`.
    * Default value: `"${workspaceFolderBasename}"`, which reads the name of the current workspace folder.

* `"program_file"`
    * Sets the name of the file to flash and debug.  This is provided in case it's needed, but for most use cases should be left at its default.  File extension must be included.
    * Default value: `${config:program_file}.elf`, which reads the `program_file` setting.

* `"OCD_interface_file"`
    * Sets the OpenOCD interface file to use.  This should match the connected debugger.  Available options can be found in the `Tools/OpenOCD/scripts/interface` folder in the MaximSDK.  
    * `.cfg` file extension must be included.
    * Default value: `cmsis-dap.cfg`

* `"OCD_target_file"`
    * Sets the OpenOCD target file to use.  This should match the target microcontroller.  Available options can be found in the `Tools/OpenOCD/scripts/target` folder in the MaximSDK.
    * `.cfg` file extension must be included.
    * Default value: `${config:target}.cfg`, which reads the `target` setting.

## Configuring the Makefile
The Makefile is the core file for the build system.  All configuration tasks such as adding source files to the build, setting compiler flags, and linking libraries are handled via the Makefile. The [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html) is a good one to have on hand.

### Adding Source Files
* The included Makefile is pre-configured for a single `main.c` source file by default.
* Additional source files can be added to the build with `SRCS += yourfile.c`
* The Makefile looks for source files _only_ in the `/src` directory by default.  If you would like to use additional source directories, add them with `VPATH += yoursourcedirectory`
* The Makefile looks for header files _only_ in the `/src` directory by default.  If you would like to use additional include directories, add them with `IPATH += yourincludedirectory`

### Compiler Flags
* Compiler flags can be added/changed via the `PROJ_CFLAGS` variable.
* Add a new flag to be passed to the compiler with `PROJ_CFLAGS += -yourflag`.  Flags are passed in the order that they are added to the `PROJ_CFLAGS` variable.

### Linking Libraries
* Additional libraries can be linked via the `PROJ_LIBS` variable.  Add a new library to the build with `PROJ_LIBS += yourlibraryname`.
    * Note : Do not include the 'lib' part of the library name, or the file extension.  For example, to link `libarm_cortexM4lf_math.a` set `PROJ_LIBS += arm_cortexM4lf_math`.
* Tell the linker where to find the library with the '-L' linker flag.  Set `PROJ_LDFLAGS += -Lpathtoyourlibrary`.  For example, set `PROJ_LDFLAGS += -L./lib` to search a 'lib' directory inside of the project for libraries. 

### Optimization Level
* The optimization level that the compiler uses can be set by changing the `MXC_OPTIMIZE_CFLAGS` variable.  See [GCC Optimization Options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html) for more details on available optimization levels.  For example, disable optimization with `MXC_OPTIMIZE_CFLAGS = -O0`

## Setting Search Paths for Intellisense
VS Code's intellisense engine must be told where to find the header files for your source code.  By default, Maxim's perpiheral drivers, the C standard libraries, and all of the sub-directories of the workspace will be searched for header files to use with Intellisense.  If VS Code throws an error on an `#include` statement (and the file exists), then a search path is most likely missing.

To add additional search paths :
1. Open the `.vscode/c_cpp_properties.json` file.  

2. Add the include path(s) to the `configurations > includePath` list.  The paths set here should contain header files, and will be searched by the Intellisense engine and when using "Go to Declaration" in the editor.

3. Add the path(s) to any relevant implementation files to the `"browse":"path"` list.  This list contains the paths that will be searched when using "Go to Definition".  

## Project Creation
**If you have not done so already, download the latest [release](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) of this repository and extract it to an accessible location.**

**For the procedures below, you will pull content from the correct sub-folder of the release of this repository.**  
* For the Maxim Micros SDK, use the contents of the `MaximSDK` folder. 
* For the LP Micros SDK, use the contents of the `MaximLP` folder.

![Release folders image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/Release_folders.JPG)

Two folders are present inside of the release package for each of the Microcontroller SDKs:  An `Inject` folder and a `New_Project` folder.
* The `Inject` folder contains an empty project template (without any source code) that you can "inject" into any directory.
* The `New_Project` folder contains a "Hello World" example project with some basic example source code.

![Sub-folders image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/Inject_and_NewProject.JPG)

As a result, there are 3 main options for project creation:
* (Option 1) Copying the pre-made "Hello World" example project.
* (Option 2) Creating a new project from scratch.
* (Option 3) Injecting into existing source code.

### Option 1.  Copying the Pre-Made Project
Copying the pre-made "Hello world" example is a great way to get rolling quickly.  Take this option if you would like to start with a (mostly) pre-configured project.

1. Copy the `New_Project` folder from the release package to an accessible location.  This will be the location of your project.

2. (Optional) Rename the folder.  For example, I might rename the folder to `MyProject`.

3. Set your target microcontroller correctly.  See [Changing the Target Microcontroller](#Changing-the-Target-Microcontroller), and then return here.

4. That's it!  This "Hello World" project can be opened with `File > Open Folder` from within VS Code and is ready to build, debug, and modify.  Some common next steps are:
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

3. Modify the Makefile to build your existing source code as necessary.  See [Configuring the Makefile](#Configuring-the-Makefile).  In the example above, I would add (at minimum) the following lines to the Makefile:

        SRCS += mysource.c
        SRCS += theirsource.c
        VPATH += ./some_library/src
        IPATH += ./some_library/include

4. With the Makefile configured for your existing source code, you'll also want to [set your target microcontroller](#Changing-the-Target-Microcontroller) correctly.

5. That's it!  The project is now configured around your existing source code, and can be opened with `File > Open Folder` from within VS Code.  Some common next steps are:
    * [Testing the Setup](#Testing-the-Setup)
    * [Building](#Building)
    * [Debugging](#Debugging)

## Testing the Setup
After creating, configuring, and opening your project with `File > Open Folder` the toolchain should be accessible from the integrated terminal.  To test that everything is working properly : 

1. Navigate to the open `TERMINAL` tab on the bottom of the VS Code application.  If a terminal is not open, you can open a new terminal with `Terminal > New Terminal` or (Ctrl+Shift+`).  

   ![Terminal image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/Terminal.JPG)

2. The following commands to retrieve version numbers should be able to be run successfully from within the terminal :

    * `make -v`
    * `openocd -v`
    * `arm-none-eabi-gcc -v`
    * `arm-none-eabi-gdb -v`
    
   For example, the `make -v` command should look like the following:
   
   ![Make -v example output](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/make_test.JPG)

# Configuration


# Building
There are 4 available build tasks that can be accessed via `Terminal > Run Build task...` or the shortcut `Ctrl+Shift+B`.

![Build Tasks Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/buildtasks.JPG)

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
The Debugger can be launched with `Run > Start Debugging`, with the shortcut `F5`, or via the `Run and Debug` window (Ctrl + Shift + D).  All standard debugging features are supported - breakpoints, watch variables, etc.  A more detailed usage guide on the debugger can be found [here](https://code.visualstudio.com/Docs/editor/debugging#_debug-actions).

Currently, there is a known issue that causes it not to automatically break on entry into main - a breakpoint must be set manually.

![Breakpoint Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/breakpoint.JPG)

To debug a project:
* Ensure that a debugger/programmer is attached between the microcontroller's debugger port and the host PC before launching a debugging session.
    * For the MAX32625PICO debugger, use the SWD port.
* Ensure that the `debugger` project config option in `settings.json` is set properly.
* Launch the debugger with `Run > Start Debugging`, with the shortcut `F5`, or via the `Run and Debug` window (Ctrl + Shift + D)
* When a debugging session is launched, the Build task will be launched automatically.  A successful build must complete before debugging.

# Known Issues
## Debugger does not automatically break on main
A breakpoint on main must be set manually before launching the debugger.

![Breakpoint Image](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/img/breakpoint.JPG)
