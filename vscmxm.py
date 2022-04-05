"""
/*******************************************************************************
* Copyright (C) 2022 Maxim Integrated Products, Inc., All Rights Reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
* IN NO EVENT SHALL MAXIM INTEGRATED BE LIABLE FOR ANY CLAIM, DAMAGES
* OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
* ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
* OTHER DEALINGS IN THE SOFTWARE.
*
* Except as contained in this notice, the name of Maxim Integrated
* Products, Inc. shall not be used except as stated in the Maxim Integrated
* Products, Inc. Branding Policy.
*
* The mere transfer of this software does not imply any licenses
* of trade secrets, proprietary technology, copyrights, patents,
* trademarks, maskwork rights, or any other form of intellectual
* property whatsoever. Maxim Integrated Products, Inc. retains all
* ownership rights.
*******************************************************************************/
"""
import argparse
import platform
import os
from generate import *

# Set up command-line args
# ---
parser = argparse.ArgumentParser(description="VSCode-Maxim command line tool.")

parser.add_argument("--os", type=str, choices=["Windows", "Linux", "RPi"], help="(Optional) Operating system to generate the project files for.  If not specified the script will auto-detect.")
parser.add_argument("--maxim_path", type=str, help="(Optional) Location of the MaximSDK.  If this is not specified then the script will attempt to use the MAXIM_PATH environment variable.")

cmd_parser = parser.add_subparsers(dest="cmd", help="sub-command", required=True)

SDK_parser = cmd_parser.add_parser("SDK", help="Populate a MaximSDK installation's example projects with VS Code project files.")

new_parser = cmd_parser.add_parser("new", help="Create a new VSCode-Maxim project")
new_parser.add_argument("location", help="Root location of the project to create.  The project will be created in a new folder located at <location>/<name>.")
new_parser.add_argument("name", help="Name of the project.  The project will be created in a new folder located at <location>/<name>.")
new_parser.add_argument("target", help="Target microcontroller for the project", choices=whitelist)
new_parser.add_argument("board", help="Target board to use for the project.")
# ---

if __name__ == "__main__":
    args = parser.parse_args()

    # Auto-detect OS
    if args.os is None:
        current_os = platform.platform()
        if "Windows" in current_os: args.os = "Windows"
        elif "Linux" in current_os: args.os = "Linux"
        else:
            print(f"{current_os} is not supported at this time.")
            exit()

    # Auto-detect MAXIM_PATH
    if args.maxim_path is None:
        # Check environment variable
        print("Checking MAXIM_PATH environment variable..")
        if "MAXIM_PATH" in os.environ.keys():
            args.maxim_path = os.environ["MAXIM_PATH"]
            print(f"MaximSDK located at {args.maxim_path}")

        else:
            print("Failed to locate the MaximSDK...  Please specify --maxim_path manually.")
            exit()
    else:
        # Parse to abs path
        args.maxim_path = os.path.abspath(args.maxim_path)

    # Process command
    if args.cmd == "SDK":
        print(f"Generating .vscode projects for all examples in SDK located at {args.maxim_path}")
        populate_maximsdk(target_os=args.os, maxim_path=args.maxim_path)

    elif args.cmd == "new":
        pass
        # TODO: new project generator


    