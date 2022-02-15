import os
import shutil
import argparse
import platform
from subprocess import run
import json

def parse_json(filename):
    """
    Parse values from a json file into a template-friendly (all-caps keys) dictionary
    """
    f = open(filename, "r")
    defaults = json.load(f)

    # Convert key values to uppercase for easier template parsing
    keys = list(defaults.keys()) # Keys are changing on the fly, so can't use a view object
    for k in keys:
        defaults[k.upper()] = defaults.pop(k)
    
    return defaults

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
    maxim_path: str = defaults["MAXIM_PATH"],
    program_file: str = defaults["PROGRAM_FILE"],
    symbol_file: str = defaults["SYMBOL_FILE"],
    M4_OCD_interface_file: str = defaults["M4_OCD_INTERFACE_FILE"],
    M4_OCD_target_file: str = defaults["M4_OCD_TARGET_FILE"],
    RV_OCD_interface_file: str = defaults["RV_OCD_INTERFACE_FILE"],
    RV_OCD_target_file: str = defaults["RV_OCD_TARGET_FILE"],
    defines: list = defaults["DEFINES"],
    i_paths: list = defaults["I_PATHS"],
    v_paths: list = defaults["V_PATHS"],
    gcc_version: str = defaults["GCC_VERSION"],
    v_xpack_gcc: str = defaults["V_XPACK_GCC"],
    OCD_path: str = defaults["OCD_PATH"],
    ARM_GCC_path: str = defaults["ARM_GCC_PATH"],
    RV_GCC_path: str = defaults["RV_GCC_PATH"],
    Make_path: str = defaults["MAKE_PATH"]
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
    i_paths_parsed = ",\n\t\t\t\t".join(tmp)  # csv, newline, and tab alignment

    # Parse browse paths...
    tmp = v_paths
    tmp = list(map("\"{0}\"".format, tmp))  # Surround with quotes
    v_paths_parsed = ",\n\t\t\t\t\t".join(tmp)  # csv, newline, and tab alignment

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
            # We're in the root template folder.
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
                            line.replace("##__MAXIM_PATH__##", maxim_path).
                            replace("##__TARGET__##", target.upper()).
                            replace("##__BOARD__##", board).
                            replace("##__PROGRAM_FILE__##", program_file).
                            replace("##__SYMBOL_FILE__##", symbol_file).
                            replace("##__M4_OCD_INTERFACE_FILE__##", M4_OCD_interface_file).
                            replace("##__M4_OCD_TARGET_FILE__##", M4_OCD_target_file).
                            replace("##__RV_OCD_INTERFACE_FILE__##", RV_OCD_interface_file).
                            replace("##__RV_OCD_TARGET_FILE__##", RV_OCD_target_file).
                            replace("\"##__I_PATHS__##\"", i_paths_parsed).  # Next 3 are surrounded in quotes in the template because of the linter
                            replace("\"##__DEFINES__##\"", defines_parsed).
                            replace("\"##__V_PATHS__##\"", v_paths_parsed).
                            replace("##__GCC_VERSION__##", gcc_version).
                            replace("##__V_XPACK_GCC__##", v_xpack_gcc).
                            replace("##__OCD_PATH__##", OCD_path).
                            replace("##__ARM_GCC_PATH__##", ARM_GCC_path).
                            replace("##__RV_GCC_PATH__##", RV_GCC_path).
                            replace("##__MAKE_PATH__##", Make_path)
                        )

                os.chmod(out_loc, 0o764)
                print(f"Wrote {os.path.basename(out_loc)}")

            else:
                # There is a non-template file to copy
                shutil.copy(os.path.join(directory, file), out_path)
                os.chmod(out_path, 0o764)
                print(f"Wrote {os.path.basename(file)}")

def populate_maximsdk(target_os, maxim_path, overwrite=True):
    print(f"Generating VS Code project files on {target_os} for MaximSDK located at {maxim_path}...")
    print(f"Scanning {maxim_path}...")

    # Search for list of targets
    targets = []
    for dir in os.scandir(os.path.join(maxim_path, "Examples")):
        if dir.name in whitelist: targets.append(dir.name)

    print(f"Generating VS Code project files for {targets}...")
    
    count = 0
    for target in targets:

        # For this target, get the list of supported boards.
        print(f"Scanning BSPs for {target}...")
        boards = []
        for dir, subdirs, files in os.walk(os.path.join(maxim_path, "Libraries", "Boards", target)):
            if "board.mk" in files: 
                boards.append(os.path.split(dir)[1])

        # Set default board.  Try EvKit_V1, otherwise use first entry in list
        board = "EvKit_V1"
        if board not in boards: board = boards[0]

        print(f"Found {boards}, using {board} as default...")

        # Search for example projects
        print(f"Searching for {target} example projects...")
        for dir, subdirs, files in os.walk(os.path.join(maxim_path, "Examples", target)):

            if "Makefile" in files:
                # Found example project

                if ".vscode" not in subdirs or (".vscode" in subdirs and overwrite):

                    print(f"Found {dir}, injecting project files...")

                    if target_os == "Windows":
                        create_project(dir, target, board, ARM_GCC_path="${config:MAXIM_PATH}/Tools/GNUTools")
                        # Windows SDK uses older GCC at different path

                    elif target_os == "Linux":
                        create_project(dir, target, board, M4_OCD_target_file=f"{str.lower(target)}.cfg") 
                        # Need to manually set MAXIM_PATH and deal with lowercase OpenOCD .cfg files on Linux.

                    count += 1

    print(f"Done!  Created {count} projects.")
    
def new():
    print("Create new project!")

parser = argparse.ArgumentParser(description="Generate Visual Studio Code project files for Maxim's Microcontroller SDK.")
parser.add_argument("--os", type=str, choices=["Windows", "Linux"], help="(Optional) Operating system to generate the project files for.  If not specified the script will auto-detect.")
parser.add_argument("--maxim_path", type=str, help="(Optional) Location of the MaximSDK.  If this is not specified then the script will attempt to use the MAXIM_PATH environment variable.")

subparsers = parser.add_subparsers(dest="cmd", help="sub-command", required=True)

sdk_parser = subparsers.add_parser("SDK", help="Populate a MaximSDK installation's example projects with VS Code project files.")

if __name__ == "__main__":
    args = parser.parse_args()

    # Auto-detect OS
    if args.os is None:
        current_os = platform.platform()
        if "Windows" in current_os: args.os = "Windows"
        elif "Linux" in current_os: args.os = "Linux"
        else:
            print(f"{current_os} is not supported at this time.  Please raise a ticket on Github requesting support for your platform.")
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

    if args.cmd == "SDK":
        populate_maximsdk(target_os=args.os, maxim_path=args.maxim_path)
