# How to Use Visual Studio Code with Maxim's Microcontrollers SDK (Windows & Linux)

## Table of Contents
* [Introduction](#introduction)
* [De-Mystifying the SDK Toolchain](#de-mystifying-the-sdk-toolchain)
* [Integrating the Toolchain](#integrating-the-toolchain)
* [Getting Started with VSCode-Maxim](#getting-started-with-vscode-maxim)
* [Referencing Example Code](#referencing-example-code)
* [Injecting into Existing Source Code](#injecting-into-existing-source-code)
* [Creating a Project from Scratch](#creating-a-project-from-scratch)

## Introduction
Integrated Development Environments (IDEs) targeted at embedded systems and microcontroller development can come with a lot of overhead.  They have a tendency to be bulky, unwieldy programs that can take up a lot of hard drive space, and when something isn't configured properly they can be a pain to troubleshoot.  No one likes digging into project settings for hours trying to get their include paths working, troubleshooting five different configuration options just to link a library, or tracking a bug back down to project config option.

[Visual Studio Code](https://code.visualstudio.com/) is a lightweight, powerful, and customizable editor that can serve as a great free alternative to the more traditional micro IDEs like Eclipse, Code-Composer Studio, IAR, Keil uVision, etc.  This app note outlines step-by-step how to get started with [VSCode-Maxim](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim), which is a collection of project configurations that integrate Maxim's Microcontrollers SDK into Visual Studio Code.

## De-Mystifying the SDK Toolchain
Maxim maintains a Software Development Kits (SDK) for microcontroller development called the "Maxim Micros SDK".  The SDK contains a large number of components, such as register files, linker files, board-support packages (BSPs), peripheral drivers, example code, etc.  This section will focus on one of the _core_ components of the SDK - the _toolchain_.

Understanding the toolchain is important because this VSCode-Maxim project is essentially a "wrapper" around the toolchain.  Let's take a look under the hood...

A [toolchain](https://en.wikipedia.org/wiki/Toolchain) is really just a collection of programs and typically includes compiler, linker, and debugger executables.  It also may include utility programs and build systems to make using these lower-level programs more convenient.

The main components of the SDK's Toolchain are:
* [Arm GNU Compiler Collection](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm) (GCC) - located under `~\MaximSDK\Tools\GNUTools\bin`
* [Open On-Chip Debugger](http://openocd.org/) (OpenOCD) - located under `~\MaximSDK\Tools\OpenOCD`
* [GNU Make](https://www.gnu.org/software/make) - made available on Windows via MSYS2 and located under `~\MaximSDK\Tools\MinGW\msys\1.0\bin`

GCC is used to compile source code but is rarely called directly.  Instead, GCC is most frequently invoked in a list of directives collected into a _Makefile_.  This list of directives is called a _recipe_.  If you are new to Make, think of GCC as the hammer and Make as the builder who knows how to use it.  You can tell Make to do a task (such as "make all" the source code) and Make will follow the instructions outlined in the Makefile's recipe to complete it.

The core Makefile for a target microcontroller can be found under `~\MaximSDK\Libraries\CMSIS\Device\Maxim\<target microcontroller>\Source\GCC` - see `gcc.mk`.  This file tells Make exactly how to use GCC to compile code for that microcontroller.  All projects can then have their own Makefile that builds off of this one by `include`-ing it.

Great - so source code is compiled into firmware binaries by Make using GCC.  How is it flashed onto the microcontroller?  That's where OpenOCD comes in.  

OpenOCD handles flashing firmware and opening a debugger _server_.  It handles the necessary configuration to support the variety of debugger adapters and debugger protocols (such as SWD or JTAG) that are available and sends debugging information and instructions to the microcontroller.  OpenOCD deals with the low-level hardware and exposes a common high-level interface that can be used with a debugger _client_ such as GDB.  GDB connects to the OpenOCD server over a socket and presents a user interface.

In general, this is how things work at a low level.  Integrated Development Environments (IDEs) such as Visual Studio Code have mechanisms for integrating toolchains so that these low-level steps can be abstracted away in a more convenient way.

## Integrating the Toolchain
Visual Studio Code provides the [Tasks](https://code.visualstudio.com/Docs/editor/tasks) interface for integrating external tools.  To use the Maxim SDK toolchain via Tasks, the toolchain binaries must be made accessible from the command line.  Additionally, the correct board and peripheral driver files for a target platform must be loaded for compilation and source code development.  When those conditions are met, then Tasks can be created to conveniently implement the features that you would expect from an IDE:  building, cleaning, flashing, etc.

[VSCode-Maxim](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim) handles this for you and offers project files that are configured for Maxim's SDK and toolchain.

Let's get started setting it up and walking through some common use-cases.  The procedure below is a demonstration for the MAX32670EVKIT running on Windows 10, but the same procedure applies to all micros and OS's.

## Getting Started with VSCode-Maxim

### 1 - Install Software Requirements
First, follow the [installation instructions](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#installation) for your OS from the readme if you haven't already.  This include installing software requirements, setting the `MAXIM_PATH` environment variable, and downloading the latest release of VSCode-Maxim to an accessible location.

<hr>

### 2 - Release Package Overview
The VSCode-Maxim release package should contain the following contents.  Note: Releases between OS's/versions may differ _slightly_ from the screenshot below, but this should match in general...

![Release Contents](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/Release-contents.jpg)

* `"Inject"` contains _just_ the VSCode-Maxim config files _without_ any source code.  It's contents are designed to be used to "inject" a VSCode-Maxim project into any folder.
* `"MaximSDK"` is used during the installation process.  Its contents can be copied into the root directory of an SDK installation to populate the SDK's example projects with VSCode-Maxim project files.
* `"New_Project"` is a starter template project with a little bit of source code.  This folder is available to make creating new VSCode-Maxim projects easier.  Copy it over to a new location and rename it to create a new starter project.
* `"LICENSE.md"` contains Maxim's copyright notice.
* `"readme.md"` is the core readme file for the project, and you should read it!
* `"userguide.md"` is this User Guide.

### 3 - Starter Project
In this section, we'll get hands on with the VSCode-Maxim starter project to see how it works.

First, copy the "New_Project" folder from the VSCode-Maxim release package into an accessible location.  You can also rename the folder if you'd like.  For example, I've copied the folder to a `workspace` directory I created in my User folder below.  I've also renamed the project to "MyProject".

**It's important that the folder name and location does _not_ contain any spaces** - this will break the project files.

![MyProject](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_location.jpg)

Now, launch Visual Studio Code.  On startup, it should look something like this:

![VSCode Startup Screen](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/VSCode-startup.jpg)

Select `Open Folder...` on the welcome page, or alternatively get there with `File -> Open Folder...`

"Open folder" is the main mechanism for opening projects in VS Code.  For those familiar with IDEs that offer options such as "New Project" or "Open Project", this may seem counterintuitive.  However, this will start to make more sense as you use it.  VS Code's editor is based entirely out of its working directory, and a `.vscode` folder inside that working directory can contain local settings overrides.  This is similar to the way `.git` folders work.

![File Open Folder](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/file_openfolder.JPG)


So...  After `File > Open Folder` navigate _inside_ of template project created earlier and click "Select Folder".

![Browse](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_openfolder.jpg)

VS Code will prompt for trust the first time.  Select _Trust folder and enable all features_.

![Trust Prompt](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/workspaceTrustPrompt.JPG)

Now, VS Code should look something like this, where the template project has been opened in the file explorer.

![File opened](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_opened.jpg)

<hr>

### 4 - Verify Toolchain Access
At this point, the project is opened and ready to use and configure.  Let's take a few steps on the integrated terminal to verify that things _are_ actually working correctly.

First, launch a terminal with `Terminal > New Terminal`.

![New Terminal](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_terminal.jpg)

Next, we'll run through the commands in the ["Testing the Setup"](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md#testing-the-setup) of the readme to see that the toolchain is accessible.  This is critical for everything else to work.  The project settings in the `.vscode` folder will add the locations of the toolchain to the terminal's `PATH`, which will allow them to be accessed directly.

For example, running `make -v` in the terminal should output a version # for Make, as shown below.

![Make Test](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/make_test.JPG)

Run the other commands for OpenOCD, GCC, and GDB to verify that the integrated terminal has been configured correctly and the toolchain is in the right place.  These should all run without error.
* `openocd -v`
* `arm-none-eabi-gcc -v`
* `arm-none-eabi-gdb -v`

If there _are_ any errors thrown by any of the commands above, first verify that you've followed the [installation instructions](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#installation) correctly.  Problems are usually related to a missing or incorrect `MAXIM_PATH` environment variable and/or missing SDK components.  Otherwise, see the [troubleshooting section](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/issues) of the readme.

<hr>

### 4 - Set the Target Platform
With the tools verified as accessible from within VS Code, we can now start to configure the project for a specific microcontroller.

In this case, we'll do some basic configuration of the project for the MAX32670EVKIT, but the same steps apply to any micro.

Open `.vscode/settings.json`.  This is the main configuration file, and you shouldn't need to interact with any of the other files inside of the `.vscode` folder except for in the most advanced use-cases.

![Opening settings.json](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/settings.JPG)

Set the `"target"` and `"board"` variables for your target platform.
For example, for the MAX32670EVKIT I would set...
* `"target":"MAX32670"`
* `"board":"EvKit_V1"`

The [Configuration](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#configuration) section of the readme will tell you the values that can be set here.  In this case, we've changed the two most basic options:  `"target"` and `"board"`.

![Basic Config Options](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/readme_basicconfig.jpg)

As shown in the readme, the value for the `"board"` option can vary.  This option sets the Board Support Package (BSP) to use, and it should match the name of a BSP folder for the target microcontroller.  BSPs for each microcontroller can be found in the `Libraries/Boards` folder of the SDK.

Save your changes to this file with `CTRL+S`.

Next, reload the VS Code window.  A reload is necessary after changing any options in `settings.json` to force a re-parse. The VS Code window can be conveniently re-loaded with the `Ctrl + Shift + P` -> `Reload Window` developer command.

![Reload window](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/reload_window.JPG)

Now VS Code is ready to edit, build, and debug source code for the target platform.

<hr>

### 5 - Opening main.c
Open `main.c`, which can be found in the `src` folder.  Here we can see the source code for a simple "Hello world" program.

![main.c](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/main.JPG)    

<hr>

### 6 - Clean the Program
First, let's ensure that we're starting from a clean slate.  Open the build tasks menu with `Ctrl+Shift+B` or `Terminal > Run Build Task...` and select the "clean-periph" option.  This cleans out the build products from the current project as well as the peripheral drivers in the SDK.  With everything cleaned out, the next step will build everything from scratch.

![Cleaning the program](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/clean-periph.jpg)

Selecting the `clean-periph` build task will launch the task in the integrated terminal, and it will look someting like this...

![Clean-periph Complete](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/clean-periph_complete.jpg)

<hr>

### 7 - Build the Program
Next, we'll build the source code.  

It should be noted that the template project's Makefile comes with a basic pre-configuration "out of the box".  However, keep in mind that the Makefile _does_ need to be edited when you want to do things like add source code, change compiler flags, etc.  This is covered in the [Editing the Makefile](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#editing-the-makefile) section of the readme and additional sections in this User Guide, but for now no additional steps are necessary - we'll see how to run the build command in the first place.

Open the build tasks menu again with `Ctrl+Shift+B` or `Terminal > Run Build Task...`

![Build Tasks](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/buildtasks_build.jpg)

Select build to compile the source code.  You'll notice the build task completing in the terminal window, and a new `build` directory will appear in the file explorer.  At the end of a successful build the program binary (.elf file) will be placed in this build directory.

![Build complete](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/build_complete.JPG)

So what happened here?

When we ran the "build" task, VS Code parsed the configuration options from `settings.json` into a `make all` command that you can see on the first line of the terminal (`Executing task: ...`).  When this command is run, Make looks inside of the project `Makefile` for the "all" recipe that tells it how to build the source code.  Remember the core GCC Makefile discussed earlier?  That's where the "all" recipe is defined.  You can open the project Makefile and see exactly where it's imported with `include`.

![Include core Makefile](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/include_core_makefile.JPG)

The source code and compiler options are passed into the build with the variables further up in the Makefile...

![Makefile main options](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/Makefile_options.JPG)

This is a good time to (once again) re-iterate an important point:  _All configuration of the build itself must be done via the project's Makefile._  [Editing the Makefile](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md#editing-the-makefile) in the readme covers this subject in more detail.

For now, take note of the fact that the example project comes  pre-configured for a single `main.c` source file, and looks for all `.c` and `.h` files inside of the `src` directory.

<hr>

### 8 - Debug the Program
Now that we've seen the program build successfully, let's flash it onto the microcontroller and debug it.

First, ensure that your microcontroller is powered on and connected to your PC through your debug adapter.  The specifics of this will vary based on the platform you're using, but documentation can be found in the datasheet.  On a platform with an integrated debugger, such as the [MAX32670EVKIT](https://datasheets.maximintegrated.com/en/ds/MAX32670EVKIT.pdf), this is as simple as plugging it in with a micro-usb cable.  On platforms where the debug adapter is not integrated, you'll need to connect your debug adapter to the right debugger port and power the platform separately.

Next, we'll flash our compiled program binaries on to the microcontroller.  This is done with the `flash` build task.  Use `CTRL + SHIFT + B` to open up the build tasks menu again and select `flash`.  The `flash` build task will automatically run the `build` task first to make sure our program has actually been compiled successfully.  `build` is incremental, so the check should only take a few seconds since we've already built the code.

Once the flash is complete, launch the debugger by pressing `F5` or by navigating to the debugger window and pressing the green play button next to "GDB".

![Debugger Window](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/debugger_window.JPG)

Once the debugger connects it will break the program execution on entry into the `main` function.  VS Code should look something like this:

![Breakpoint Hit](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/breakpoint_hit.JPG)

<hr>

### 11 (optional) - Open a Serial Port to the Micro
Before we continue the program execution, you can optionally open up a serial port to the microcontroller to see the "Hello world!" message and count printed.

Default serial communication settings are:
* BAUD : 115200
* Data : 8-bit
* Parity : none
* Stop bits : 1 bit
* Flow control : none

[TeraTerm](https://ttssh2.osdn.jp/index.html.en) and [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/) are good serial terminal program options.  To open a serial port to the microcontroller with one of these programs you'll first need to find the COM port associated with the debugger.  On Windows, this will show up as a generic USB Serial Device:

![COM port](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/78000_COM_port.JPG)

From there, steps will be program-specific to the serial terminal you're using.  For example, using TeraTerm I can navigate to `Setup -> Serial port...` to enter the communication settings above and open the connection.

![TeraTerm](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/TeraTerm.JPG)

<hr>

### 12 - Continue the Program
Press `F5` or hit the continue button in the debugger menu to continue the program past the breakpoint.

![Continue button](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/continue_button.JPG)

You should see the LED on your microcontroller blinking.  If you have a terminal window open you should also see the "Hello World" message and count being printed.

![Hello World Terminal](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/helloworld_terminal.JPG)

Feel free to play around in the debugger here (setting different breakpoints, watch variables, stepping into and out of functions, etc.) to get familiar.  When you're ready, you can hit the stop button to quit debugging.

<hr>

### 13 - Wrapping Up
Here, we've gotten started with a basic project configuration, the available build tasks, and have debugged a Hello World program.  The `New_Project` folder is intended as a project template to get you started, and you can freely copy this project around and re-configure it for different target platforms.

You should now have a good basic understanding of how VS Code works and how Maxim's toolchain is integrated.  The next sections cover more advanced subjects.

<hr>

## Referencing Example Code
When writing code for Maxim's Microcontrollers you might want to reference example code to see how to use our peripheral drivers.

In the MaximSDK examples can be found under the `~\MaximSDK\Examples\<Target Platform>` folder, and in the LP SDK they can be found under the `~\Maxim\Firmware\<Target Platform>\Applications\EvKitExamples` folder.  For instance, the MAX32670 has the following examples available:

![Examples folder](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/examples_folder.JPG)

Opening the GPIO example reveals the following contents:

![GPIO Contents](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_contents.JPG)

There are a couple components inside the project:
* A `main.c` file with the example code
* A project `Makefile` for building the example code
* Eclipse configuration files and debugger profile (`.cproject`, `.project`, `GPIO.launch`)
* A readme

_(Before proceeding - This section assumes you've already met the [requirements](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#requirements) for using the VSCode-Maxim repository.  If not, working through the "Getting Started" section of this UG first is recommended.)_

A quick way to reference the example code is to drag and drop it into VS Code's editor while you have an active project open.  Intellisense settings for the active project will be used even when editing external files.  For example, dragging the `main.c` file from the GPIO example for the MAX32670 into the "Hello World" project we configured in the previous section allows for simultaneous viewing.

![GPIO Copy](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/GPIO_copy.JPG)

![GPIO Imported](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_imported.JPG)

This provides a convenient way to reference the example code for your own application, and since Intellisense look-ups are loaded from our currently active project go-to definitions are supported.  For example, we can open the header file for the GPIO driver itself...

(Right click on `"gpio.h"` -> Go to Definition)

![GPIO Goto](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_goto.JPG)

... and see that the correct header file from the peripheral drivers is opened.

![GPIO Header](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_header.JPG)

If you want to dig in deeper and see how the peripheral driver functions are implemented at the register level, you can do so as well.  For example, we can look at the implementation of the `MXC_GPIO_Init` function.

![GPIO Init](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_init_rightclick.JPG)

The implementation file for the correct die-type of the microcontroller needs to be selected (in the case of the MAX32670 that's the ME21), and then the function definition can be viewed.  Double click on the function definition to open the full file view.

![GPIO Implementation File](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_init_implementation.JPG)

Using this method, you can quickly and easily reference example code for your own applications.  This method works for any external code, provided that the search paths for Intellisense are configured properly.  For more details on configuration of those search paths, see the [readme](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md).

## Injecting into Existing Source Code
Using example code as a reference is great, but what if we want to work with it directly, or inject the VS Code setup into a different project that's not in the MaximSDK?  That's where the `Inject` folder in the VSCode-Maxim release package comes in.  In the example below, we'll inject the VS Code setup into the Maxim SDK GPIO example, but this procedure fundamentally applies to any existing source code.

_This section assumes you've already met the [requirements](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#requirements) for using the VSCode-Maxim repository.  If not, working through the "Getting Started" section of this UG first is recommended._

### 1 - Locate the Existing Project
Example projects can be found under the `~\MaximSDK\Examples\<Target Platform>` folder for the Maxim SDK and in the LP SDK they can be found under the `~\Maxim\Firmware\<Target Platform>\Applications\EvKitExamples` folder.  For the sake of this example, a working copy of the GPIO example has been copied over into a separate folder.

The contents of this GPIO example are as follows:

![GPIO Contents](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_contents.JPG)

<hr>

### 2 - (Optional) Delete Eclipse Project Files
The `.cproject`, `.project`, and `GPIO.launch` files are all Eclipse-related project files.  Since we're working with VS Code these can be deleted to clean up the project.

![GPIO Contents Cleaned](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_contents_clean.JPG)

<hr>

### 3 - (Optional) Rename the Existing Makefile
In step #4 we'll inject the VS Code setup into the project folder, and this will replace the existing Makefile.  It may good idea to keep the existing Makefile around for reference, especially for more complicated projects.

Rename the existing `Makefile` to `Makefile-old` to keep a reference copy.  By renaming the file, it won't interfere with our new one.

![Rename Makefile](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/rename_makefile.JPG)

<hr>

### 4 - Inject the VS Code Environment
Copy the _contents_ of the `Inject` for your SDK from VSCode-Maxim into the example project.  In this example we're working with the MAX32670, so we'll use the `Inject` folder inside of the `MaximSDK` folder.  

![GPIO Inject](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/inject_gpio.JPG)

The contents of the project should now look something like this, with our `.vscode` folder and new `Makefile`.

![GPIO Injected](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/inject_gpio_finished.JPG)

<hr>

### 5 - Open the Project
The GPIO is now ready to be opened from within VS Code, and from here we'll follow a similar process as the one outlined in the "Getting Started" section of this User Guide.  You'll open the project folder and configure `settings.json` for your target platform.  However, since we're injecting into existing source code, we'll need to configure the build system a bit as well.  We'll get into that, but first things first...

Launch VS Code.  Open the project folder with `File > Open Folder...` and browse to the root directory of the project.

![GPIO Root](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_root.JPG)

VS Code should prompt for workspace trust.  Select _Trust folder and enable all features_.

![Workspace Trust Prompt](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/workspaceTrustPrompt.JPG)

<hr>

### 6 - Set the Target Platform & Reload
Open `settings.json` inside of the `.vscode` folder and configure the project settings for your target platform.  See the [readme](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md) if you are unsure what to set here.  
For example, settings for the MAX32670EVKIT would be...
* `"target":"MAX32670"`
* `"board":"EvKit_V1"`
* `"debugger":"cmsis-dap"`

`CTRL+S` to save the changes to the file, and then reload the VS Code window with `CTRL + SHIFT + P` > `Developer: Reload Window`.  This is necessary so that VS Code re-parses all file-paths for our new target platform.

![Reload Window](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_reload_window.JPG)

<hr>

### 7 - Configure the Build System
With the project settings configured, everything should be working in the editor.  The `main.c` file can be opened and Intellisense will work properly.

However, in order to actually build this project, we'll need to configure the build system to match the existing source code.  This involves editing the core project `Makefile`.

Open the `Makefile` in the editor.

![Open Makefile](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_open_makefile.JPG)

Here, we can see a "Main Configuration" section highlighting some common options that, collectively, handle the configuration needed for most projects.  The first thing to check is that all the source files have been added to the `SRCS` variable.  The GPIO project only has a single `main.c` file, and the Makefile comes pre-configured for a `main.c` file by default.  So, we're good to go there.

However, if we look at the `VPATH` and `IPATH` options we can see some modifications are required.  `VPATH` controls where Make will look for the source files (.c) specified by the `SRCS` variable, and `IPATH` controls where it will look for header files (.h).  The GPIO example has placed the `main.c` file right in the root directory of the project but the Makefile is only configured to look inside of a `src` folder by default.  So we have two options:
1. Re-organize the existing source code to match the Makefile.
    * Create a new folder inside of the project called `src`
    * Drag `main.c` inside of that folder

    ![GPIO Reorganized](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_reorganized.JPG)

or...

2. Re-configure the Makefile to match the existing source code.  
    * Set `VPATH` and `IPATH` to `.` to search the root directory for source and header files.

    ![Makefile Edited](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_makefile_edited.JPG)

<hr>

### 8 - Clean & Build the GPIO Example
With the Makefile configured, we're ready to build the project.

As always, with a new project it's best to run a `clean-periph` first to ensure we're starting from scratch.  

Then, run a `build` task to compile the GPIO example.  Remember - build tasks can be accessed via `Terminal > Run Build Task...` or `Ctrl+Shift+B`.

![Build Tasks](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/buildtasks.JPG)

Monitor the terminal for any errors as the Makefile builds the periphal drivers and the GPIO example source code.  A successful build will look something like this, ultimately linking everything into our final `.elf` file...

![GPIO Build](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_build.JPG)

... with our build products and final program binary output inside of a `build` folder.

![GPIO Build Products](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/gpio_build_products.JPG)

<hr>

### 9 - Wrapping Up
From here, the example is ready to be flashed to the target microcontroller, debugged, edited, and explored further.  This same process can be applied to injecting the VS Code setup into any example project or existing source code.  

To summarize, you will...
1. Copy the contents of the `Inject` folder into the root directory of the existing project (optionally renaming any existing Makefile for later reference).
2. Open the root directory of the project folder from within VS Code
3. Configure `settings.json` to match your target platform
4. Configure the Build system by editing the Makefile and/or re-organizing the source code.

<hr>

## Creating a Project from Scratch
In the previous sections we've gotten started with the "Hello World" example, discussed how to reference example code, and demonstrated injecting the VS Code setup into existing source code.  Working through these examples should give you an idea of what might be involved with creating a new project from scratch, but it's helpful to have a clear procedure and example to reference.  In the example below, we'll walk through building up a simple program from scratch.  This program will have a more advanced project structure with additional source files and sub-folders.

_This section assumes you've already met the [requirements](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim#requirements) for using the VSCode-Maxim repository.  If not, working through the "Getting Started" section of this UG first is recommended._

### 1 - Create the Project Folder
To start, create a new folder for the project.  The only requirements for this folder are that it's...
* Accessible
* Doesn't have any spaces in the full directory path

In this example, I've created a folder called `MyProject`.

![My Project](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_empty.JPG)

<hr>

### 2 - Inject VSCode-Maxim into the Project Folder
Next, copy the contents of the `Inject` folder for your target platform from [VSCode-Maxim](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/releases) into the newly created project folder.  If you're unsure which folder to use (`MaximLP` vs `MaximSDK`) consult the [readme](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md).

In the example below, I'll be building a project for the MAX32670EVKIT.  So the `Inject` folder from `MaximSDK` will be used.

![Inject into MyProject](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_inject.JPG)

The contents of the new project should now look as follows...

![Injected into MyProject](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_injected.JPG)

<hr>

### 3 - Open the Folder in VS Code
Launch VS Code and open the project folder with `File > Open Folder`.

VS Code should prompt for trust the first time you open the project.  Select _Trust folder and enable all features_.

<hr>

### 4 - Set the Target Platform & Reload
Open `settings.json` inside of the `.vscode` folder and configure the project settings for your target platform.  See the [readme](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md) if you are unsure what to set here.  
For example, settings for the MAX32670EVKIT would be...
* `"target":"MAX32670"`
* `"board":"EvKit_V1"`
* `"debugger":"cmsis-dap"`

`CTRL+S` to save the changes to the file, and then reload the VS Code window with `CTRL + SHIFT + P` > `Developer: Reload Window`.  This is necessary so that VS Code re-parses all file-paths for our new target platform.

![Reload Window](img/myproject_reload.JPG)

<hr>

### 5 - Create a 'src' Directory
Next, create a folder inside of the project called `src`.  The Makefile is pre-configured to look for source files inside of this folder by default.  It's recommended to use this configuration, but if you would like you can change the `VPATH` and `IPATH` assignments inside of the project `Makefile`.

![VPATH and IPATH](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/vpath_ipath.JPG)

Right click in VS Code's explorer and select "New Folder".

![New Folder](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_newfolder.JPG)

Name the folder "src" to match the Makefile configuration.

![Src Folder](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_src.JPG)

<hr>

### 6 - Create a 'main.c' File
Next, create a `main.c` file inside of the newly created `src` folder.  This file will contain the `main` entry-point function of the program.

Right click on the `src` folder and select "New File".

![New File](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_newfile.JPG)

Name it `main.c` and hit Enter.  It should open in the editor.

<hr>

### 7 - Define a 'main' Function
Define the standard `main` function that will be the entry-point to the program.

![Main function](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_main_empty.JPG)

Fundamentally, that's it.  The project is ready to be built, debugged, and expanded.  Remember:  When starting a new project, it's a good idea to run `clean-periph` once to ensure you're building the peripheral drivers from scratch.

For the sake of this example we'll continue and add in some additional source code to demonstrate additional configuration of the build system.

<hr>

### 8 - Adding Additional Source Code
Adding and editing additional source code to the project is straightforward.  Files can be created from within VS Code or dragged and dropped into the project explorer.  However, the `Makefile` must be configured properly to add any additional source code to the build.

There are some general rules that can be followed for configuring the `Makefile`:
* Make sure the any implementation files added (.c) are added to the list of files to compile with the `SRCS` variable.
* Make sure the `Makefile` knows where to find these implementation files.  You control where it looks with the `VPATH` variable.
* Header files (.h) don't need to be explicitly added to the build like source files (.c) do, but the `Makefile` needs to know where to look for them.  You control where it looks with the `IPATH` variable.

For example, let's say I add the following source code in its own folder called `mylibrary`, with a `hellolibrary` header (.h) and implementation (.c) file.

![Hello Library h](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_hellolibrary_h.JPG)

![Hello Library c](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_hellolibrary_c.JPG)

All this library does is contain a function called `myfunction` that prints a string to the console.  Our main file can `#include` the header file and call `myfunction()`, which will print "Hello function!" to the console.

![Hello Library main](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_hellolibrary_main.JPG)

For this source code, we'll then modify the `Makefile` to add it to the build as follows:
* `SRCS += hellolibrary.c` to add the implementation file to the build
* `VPATH += ./src/mylibrary` so the `Makefile` knows where to find the implementation file
* `VPATH += ./src/mylibrary` so the `Makefile` knows where to find the header file.

![Hello Library Makefile](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_hellolibrary_makefile.JPG)

Now, when we run the `Build` task we can see the hellolibrary.c file added to the build successfully and compiled.  The program is ready to be flashed to the microcontroller and debugged, where it will print "Hello function!" once to the serial port before exiting.

![MyProject Build](https://raw.githubusercontent.com/MaximIntegratedTechSupport/VSCode-Maxim/main/img/myproject_build.JPG)

<hr>

### 9 - Wrapping Up
Above, we've seen how to build up a project from scratch and how to expand it with additional source code.  The procedure outlined here for configuring the Makefile will be suitable for most situations but hasn't covered everything.  For a more detailed list of configuration options, see the [readme](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/blob/main/readme.md).

<hr>

## Conclusion
Visual Studio Code is a great free code editor that, with the help of [VSCode-Maxim](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim), can be used for embedded development with Maxim's Microcontroller toolchain.  Having worked through this User Guide, you now hopefully have a good understanding of how Maxim's toolchain works, how it's integrated into VS Code, and how to leverage it to develop your own projects.

Bug reports, feature requests, and contributions are welcome via the [issues](https://github.com/MaximIntegratedTechSupport/VSCode-Maxim/issues) tracker on Github.
