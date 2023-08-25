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

import sys, os
import shutil
import stat
# from utils import *
from . import utils
from pathlib import Path
from .maintain import sync

# Get location of this file.
# Need to use this so that template look-ups are decoupled from the caller's working directory 
if getattr(sys, 'frozen', False):
    # https://pyinstaller.org/en/stable/runtime-information.html#run-time-information
    # Use sys.executable if app is bundled by pyinstaller
    here = Path(sys.executable).parent
    _defaults = here.joinpath("VSCode/MaximSDK/Inject/.vscode/settings.json")
    template_dir = here.joinpath("VSCode/MaximSDK/Template").resolve()
else:
    here = Path(__file__).parent
    _defaults = here.joinpath("MaximSDK/Inject/.vscode/settings.json")
    template_dir = here.joinpath("MaximSDK/Template").resolve()

# Load default values for template from master "inject" folder so that we don't have to maintain multiple copies of the settings
defaults = utils.parse_json(_defaults)

synced=False

whitelist = [
    "MAX32650",
    "MAX32655",
    "MAX32660",
    "MAX32662",
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
    out_root: str,
    out_stem: str,
    target: str,
    board: str,
    overwrite = False,
    backup = False,
    program_file: str = defaults["PROGRAM_FILE"],
    symbol_file: str = defaults["SYMBOL_FILE"],
    m4_ocd_interface_file: str = defaults["M4_OCD_INTERFACE_FILE"],
    m4_ocd_target_file: str = defaults["M4_OCD_TARGET_FILE"],
    rv_ocd_interface_file: str = defaults["RV_OCD_INTERFACE_FILE"],
    rv_ocd_target_file: str = defaults["RV_OCD_TARGET_FILE"],
    defines: list = defaults["C_CPP.DEFAULT.DEFINES"],
    i_paths: list = defaults["C_CPP.DEFAULT.INCLUDEPATH"],
    v_paths: list = defaults["C_CPP.DEFAULT.BROWSE.PATH"],
    v_arm_gcc: str = defaults["V_ARM_GCC"],
    v_xpack_gcc: str = defaults["V_XPACK_GCC"],
    ocd_path: str = defaults["OCD_PATH"],
    arm_gcc_path: str = defaults["ARM_GCC_PATH"],
    xpack_gcc_path: str = defaults["XPACK_GCC_PATH"],
    make_path: str = defaults["MAKE_PATH"],
    msys_path: str = defaults["MSYS_PATH"]
):
    """
    Generates Visual Studio Code project files from the VSCode-Maxim project.
    """

    global synced
    if not synced:
        sync()
        synced = True

    out_path = Path(out_root).joinpath(out_stem)

    template_prefix = "template"
    # Filenames beginning with this will have substitution

    if not template_dir.exists():
        raise Exception(f"Failed to find project template folder '{template_dir}'.")

    tmp = []  # Work-horse list, linter be nice
    # Parse compiler definitions...
    if defines != []:
        tmp = defines
        tmp = list(map(lambda s: s.strip("-D"), tmp))  # VS Code doesn't want -D
        tmp = list(map(lambda s: f"\"{s}\"", tmp))  # Surround with quotes
        defines_parsed = ",\n        ".join(tmp)  # csv, newline, and tab (w/ spaces) alignment
    else:
        defines_parsed = ""

    # Parse include paths...
    tmp = i_paths
    tmp = list(map(lambda s: f"\"{s}\"", tmp))  # Surround with quotes
    i_paths_parsed = ",\n        ".join(tmp).replace(target, "${config:target}").replace("\\", "/")

    # Parse browse paths...
    tmp = v_paths
    tmp = list(map(lambda s: f"\"{s}\"", tmp))  # Surround with quotes
    v_paths_parsed = ",\n        ".join(tmp).replace(target, "${config:target}").replace("\\", "/")

    updated = []
    # Create template...
    for directory, _, files in sorted(os.walk(template_dir)):
        # ^ For each directory in the directory tree rooted at top (including top itself,
        # but excluding '.' and '..'), yields a 3-tuple (dirpath, dirnames, filenames)

        # Get current directory relative to root
        rel_dir = Path(directory).relative_to(Path(template_dir))

        # Figure out whether we're in a subfolder of the template directory,
        # and form output path accordingly.
        if rel_dir != Path('.'):
            # We're in a sub-folder.  Replicate this folder in the output directory
            out_path = Path(out_path).joinpath(rel_dir)
            os.makedirs(out_path, exist_ok=True)
        else:
            # We're in the root template folder, no need to create a directory.
            pass

        
        # Any files to copy?
        for file in sorted(files):

            if file.startswith(template_prefix):

                # There is a template file to copy.  Perform string substitution in output file.
                out_file = Path(out_path).joinpath(file[len(template_prefix):])  # Remove prefix
                template = Path(directory).joinpath(file)

                content = None
                with open(template, 'r', encoding="UTF-8") as f:
                    content = f.read()
                    content = content.replace("##__TARGET__##", target.upper()). \
                        replace("##__BOARD__##", board). \
                        replace("##__PROGRAM_FILE__##", program_file). \
                        replace("##__SYMBOL_FILE__##", symbol_file). \
                        replace("##__M4_OCD_INTERFACE_FILE__##", m4_ocd_interface_file). \
                        replace("##__M4_OCD_TARGET_FILE__##", m4_ocd_target_file). \
                        replace("##__RV_OCD_INTERFACE_FILE__##", rv_ocd_interface_file). \
                        replace("##__RV_OCD_TARGET_FILE__##", rv_ocd_target_file). \
                        replace("\"##__I_PATHS__##\"", i_paths_parsed). \
                        replace("\"##__DEFINES__##\"", defines_parsed). \
                        replace("\"##__V_PATHS__##\"", v_paths_parsed). \
                        replace("##__V_ARM_GCC__##", v_arm_gcc). \
                        replace("##__V_XPACK_GCC__##", v_xpack_gcc). \
                        replace("##__OCD_PATH__##", ocd_path). \
                        replace("##__ARM_GCC_PATH__##", arm_gcc_path). \
                        replace("##__XPACK_GCC_PATH__##", xpack_gcc_path). \
                        replace("##__MAKE_PATH__##", make_path). \
                        replace("##__MSYS_PATH__##", msys_path)

                write = True
                if out_file.exists():
                    if not overwrite or utils.compare_content(content, out_file):
                        write = False

                if write:
                    with open(out_file, "w+", encoding="UTF-8") as f:
                        f.write(content)
                    os.chmod(out_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
                    if out_file not in updated:
                        updated.append(out_file)

                    # print(f"Wrote {os.path.basename(out_loc)}")  # Uncomment to debug

            else:
                # There is a non-template file to copy
                in_file = Path(directory).joinpath(file)
                out_file = Path(out_path).joinpath(file)
                
                write = True
                if out_file.exists():
                    if not overwrite or (utils.hash_file(in_file) == utils.hash_file(out_file)):
                        write = False

                if write:
                    if backup and out_file.exists():
                        shutil.copy(out_file, out_path.joinpath(f"{out_file.name}.backup"))
                    shutil.copy(in_file, out_path)
                    os.chmod(out_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
                    if out_file not in updated:
                        updated.append(out_file)
                    # print(f"Wrote {os.path.basename(file)}") # Uncomment to debug

    return (len(updated) > 0)
