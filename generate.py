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

import os
import shutil
import argparse
import platform
from subprocess import run
from utils import parse_json
from sdk import *

# Load default values for template from master "inject" folder so that we don't have to maintain multiple copies of the settings
defaults = parse_json("MaximSDK/Inject/.vscode/settings.json")
c_cpp_properties = parse_json("MaximSDK/Inject/.vscode/c_cpp_properties.json")
win32 = dict(c_cpp_properties["CONFIGURATIONS"][0]) # Win32 configuration is always first

defaults["DEFINES"] = win32["defines"]
defaults["I_PATHS"] = win32["includePath"]
defaults["V_PATHS"] = win32["browse"]["path"]

whitelist = [
    "MAX32650",
    "MAX32655",
    "MAX32660",
    "MAX32665",
    "MAX32670",
    "MAX32672",
    "MAX32675",
    "MAX32680",
    "MAX32690",
    "MAX78000",
    "MAX78002"
]

def create_project(
    out_path: str,
    target: str,
    board: str,
    program_file: str = defaults["PROGRAM_FILE"],
    symbol_file: str = defaults["SYMBOL_FILE"],
    m4_ocd_interface_file: str = defaults["M4_OCD_INTERFACE_FILE"],
    m4_ocd_target_file: str = defaults["M4_OCD_TARGET_FILE"],
    rv_ocd_interface_file: str = defaults["RV_OCD_INTERFACE_FILE"],
    rv_ocd_target_file: str = defaults["RV_OCD_TARGET_FILE"],
    defines: list = defaults["DEFINES"],
    i_paths: list = defaults["I_PATHS"],
    v_paths: list = defaults["V_PATHS"],
    v_arm_gcc: str = defaults["V_ARM_GCC"],
    v_xpack_gcc: str = defaults["V_XPACK_GCC"],
    ocd_path: str = defaults["OCD_PATH"],
    arm_gcc_path: str = defaults["ARM_GCC_PATH"],
    xpack_gcc_path: str = defaults["XPACK_GCC_PATH"],
    make_path: str = defaults["MAKE_PATH"]
):

    template_dir = os.path.abspath(os.path.join("MaximSDK", "Template"))  # Where to find the VS Code template directory relative to this script
    template_prefix = "template"  # Filenames beginning with this will have substitution

    if not os.path.exists(template_dir):
        raise(Exception(f"Failed to find project template folder '{template_dir}'.  Check the location and existence of these files."))

    tmp = []  # Work-horse list, linter be nice
    if defines != []:
        # Parse defines...
        # ---
        tmp = defines
        tmp = list(map(lambda s: s.strip("-D"), tmp))  # VS Code doesn't want -D
        tmp = list(map("\"{0}\"".format, tmp))  # Surround with quotes
        defines_parsed = ",\n\t\t\t\t".join(tmp)  # csv, newline, and tab alignment
        # ---
    else:
        defines_parsed = ",\n\t\t\t\t".join(defines)

    # Parse include paths...
    tmp = i_paths
    tmp = list(map("\"{0}\"".format, tmp))  # Surround with quotes
    i_paths_parsed = ",\n\t\t\t\t".join(tmp).replace(target, "${config:target}").replace("\\", "/")


    # Parse browse paths...
    tmp = v_paths
    tmp = list(map("\"{0}\"".format, tmp))  # Surround with quotes
    v_paths_parsed = ",\n\t\t\t\t\t".join(tmp).replace(target, "${config:target}").replace("\\", "/")  # csv, newline, and tab alignment

    # Create template...
    for directory, _, files in sorted(os.walk(template_dir)):
        # ^ For each directory in the directory tree rooted at top (including top itself,
        # but excluding '.' and '..'), yields a 3-tuple (dirpath, dirnames, filenames)

        # Get current directory relative to root
        rel_dir = os.path.relpath(directory, template_dir)

        # Figure out whether we're in a subfolder of the template directory,
        # and form output path accordingly.
        if rel_dir != '.':
            # We're in a sub-folder.  Replicate this folder in the output directory
            out_path = os.path.join(out_path, rel_dir)
            os.makedirs(out_path, exist_ok=True)
        else:
            # We're in the root template folder, no need to create a directory.
            pass

        # Any files to copy?
        for file in sorted(files):

            if file.startswith(template_prefix):

                # There is a template file to copy.  Perform string substitution in output file.
                out_loc = os.path.join(out_path, file[len(template_prefix):])
                with open(os.path.join(directory, file)) as in_file, \
                        open(out_loc, "w+") as out_file:
                    for line in in_file.readlines():
                        out_file.write(
                            line.replace("##__TARGET__##", target.upper()).
                            replace("##__BOARD__##", board).
                            replace("##__PROGRAM_FILE__##", program_file).
                            replace("##__SYMBOL_FILE__##", symbol_file).
                            replace("##__M4_OCD_INTERFACE_FILE__##", m4_ocd_interface_file).
                            replace("##__M4_OCD_TARGET_FILE__##", m4_ocd_target_file).
                            replace("##__RV_OCD_INTERFACE_FILE__##", rv_ocd_interface_file).
                            replace("##__RV_OCD_TARGET_FILE__##", rv_ocd_target_file).
                            replace("\"##__I_PATHS__##\"", i_paths_parsed).  # Next 3 are surrounded in quotes in the template because of the linter
                            replace("\"##__DEFINES__##\"", defines_parsed).
                            replace("\"##__V_PATHS__##\"", v_paths_parsed).
                            replace("##__V_ARM_GCC__##", v_arm_gcc).
                            replace("##__V_XPACK_GCC__##", v_xpack_gcc).
                            replace("##__OCD_PATH__##", ocd_path).
                            replace("##__ARM_GCC_PATH__##", arm_gcc_path).
                            replace("##__XPACK_GCC_PATH__##", xpack_gcc_path).
                            replace("##__MAKE_PATH__##", make_path)
                        )

                os.chmod(out_loc, 0o764)
                # print(f"Wrote {os.path.basename(out_loc)}")  # Uncomment to debug

            else:
                # There is a non-template file to copy
                shutil.copy(os.path.join(directory, file), out_path)
                os.chmod(out_path, 0o764)
                #print(f"Wrote {os.path.basename(file)}") # Uncomment to debug

@time_me
def populate_maximsdk(target_os, maxim_path, overwrite=True):
    # Copy readme into template directory
    shutil.copy("readme.md", str(Path("MaximSDK/Template/.vscode/")))

    print(f"Scanning {maxim_path}...")

    # Check for cache file
    cachefile = Path(maxim_path).joinpath(".cache").joinpath("msdk")

    if (cachefile.exists()):
        print("Loading from cache file...")
        sdk = SDK.thaw(cachefile)
    else:
        sdk = SDK.from_search(maxim_path)
        sdk.freeze(cachefile)
    
    count = 0
    for example in sdk.examples:
        #print(f"Generating VSCode-Maxim project for {example.path} ...")

        # Common options
        _path = example.path
        _target = example.target.name
        _board = example.target.boards[0].name # Default to first board in list
        for b in example.target.boards:
            # Use EvKit_V1 if possible.
            # Some boards modify EvKit_V1 (ex: QN_EvKit_V1)
            if "EvKit_V1" in b.name: _board = b.name 
            
        _program_file="${config:project_name}-combined.elf" if example.riscv else defaults["PROGRAM_FILE"]
        _symbol_file="${config:project_name}.elf" if example.riscv else defaults["SYMBOL_FILE"]
        _ipaths = [] + defaults["I_PATHS"]
        _vpaths = [] + defaults["V_PATHS"]

        # Add include and browse paths for the libraries that this example uses
        for l in example.libs:
            for ipath in l.get_ipaths(example.target.name):
                _ipaths.append(
                    str(ipath.as_posix()).
                    replace(sdk.maxim_path.as_posix(), "${config:MAXIM_PATH}").
                    replace(example.target.name, "${config:target}")
                )

            for vpath in l.get_vpaths(example.target.name):
                _vpaths.append(
                    str(vpath.as_posix()).
                    replace(sdk.maxim_path.as_posix(), "${config:MAXIM_PATH}").
                    replace(example.target.name, "${config:target}")
                )

        # Linux OpenOCD .cfg files are case senstive.  Need to hard-code a lowercase value.
        _m4_ocd_target_file = f"{str.lower(example.target.name)}.cfg" if target_os == "Linux" else defaults["M4_OCD_TARGET_FILE"]

        # RPi Tools
        if target_os == "RPi":
            _arm_gcc_path = "${config:MAXIM_PATH}/Tools/GNUTools/gcc-arm-none-eabi/${config:v_Arm_GCC}"
            _xpack_gcc_path = "${config:MAXIM_PATH}/Tools/xPack/riscv-none-embed-gcc/${config:v_xPack_GCC}"
            _v_arm_gcc = "10.3.1"
            _v_xpack_gcc = "10.2.0-1.2"
        else:
            _arm_gcc_path = defaults["ARM_GCC_PATH"]
            _xpack_gcc_path = defaults["XPACK_GCC_PATH"]
            _v_arm_gcc = defaults["V_ARM_GCC"]
            _v_xpack_gcc = defaults["V_XPACK_GCC"]

        create_project(
            _path,
            _target,
            _board,
            program_file=_program_file,
            symbol_file=_symbol_file,
            i_paths=_ipaths,
            v_paths=_vpaths,
            m4_ocd_target_file=_m4_ocd_target_file,
            arm_gcc_path=_arm_gcc_path,
            xpack_gcc_path=_xpack_gcc_path,
            v_arm_gcc=_v_arm_gcc,
            v_xpack_gcc=_v_xpack_gcc
        )

        count += 1

    print(f"Done!  Created {count} projects.")
