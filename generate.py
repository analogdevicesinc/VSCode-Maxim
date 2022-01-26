import os
import shutil
import platform

defaults = {
    "MAXIM_PATH":"${env:MAXIM_PATH}", 
    "PROGRAM_FILE":"${config:project_name}.elf",
    "SYMBOL_FILE":"${config:program_file}",
    "M4_OCD_INTERFACE_FILE":"cmsis-dap.cfg",
    "M4_OCD_TARGET_FILE":"${config:target}.cfg",
    "RV_OCD_INTERFACE_FILE":"ftdi/olimex-arm-usb-ocd-h.cfg",
    "RV_OCD_TARGET_FILE":"${config:target}-riscv.cfg",
    "DEFINES":[
        "${config:board}"
    ],
    "I_PATHS":[
        "${workspaceFolder}/**",
        "${config:MAXIM_PATH}/Libraries/PeriphDrivers/Include/${config:target}",
        "${config:MAXIM_PATH}/Libraries/Boards/${config:target}/Include",
        "${config:MAXIM_PATH}/Libraries/Boards/${config:target}/${config:board}/Include",
        "${config:MAXIM_PATH}/Libraries/CMSIS/Device/Maxim/${config:target}/Include",
        "${config:MAXIM_PATH}/Libraries/CMSIS/Include",
        "${config:MAXIM_PATH}/Tools/GNUTools/arm-none-eabi/include",
        "${config:MAXIM_PATH}/Tools/GNUTools/lib/gcc/arm-none-eabi/9.2.1/include"
        ],
    "V_PATHS":[
        "${workspaceFolder}",
        "${config:MAXIM_PATH}/Libraries/PeriphDrivers/Source",
        "${config:MAXIM_PATH}/Libraries/Boards/${config:target}/Source",
        "${config:MAXIM_PATH}/Libraries/Boards/${config:target}/${config:board}/Source"
    ],
    "GCC_VERSION":"10.3.1",
    "OCD_PATH":"${config:MAXIM_PATH}/Tools/OpenOCD",
    "ARM_GCC_PATH":"${config:MAXIM_PATH}/Tools/GNUTools/gcc-arm-none-eabi-${config:GCC_version}",
    "RV_GCC_PATH":"{config:MAXIM_PATH}/Tools/xPack/riscv-none-embed-gcc",
    "MAKE_PATH":"${config:MAXIM_PATH}/Tools/MinGW/msys/1.0/bin"
}

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
    OCD_path: str = defaults["OCD_PATH"],
    ARM_GCC_path: str = defaults["ARM_GCC_PATH"],
    RV_GCC_path: str = defaults["RV_GCC_PATH"],
    Make_path: str = defaults["MAKE_PATH"]
):

    template_dir = os.path.join("MaximSDK", "Template")  # Where to find the VS Code template directory relative to this script
    template_prefix = "template"  # Filenames beginning with this will have substitution

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
                            replace("##__OCD_PATH__##", OCD_path).
                            replace("##__ARM_GCC_PATH__##", ARM_GCC_path).
                            replace("##__RV_GCC_PATH__##", RV_GCC_path).
                            replace("##__MAKE_PATH__##", Make_path)
                        )

            else:
                # There is a non-template file to copy
                shutil.copy(os.path.join(directory, file), out_path)
                
def generate_maximsdk(maxim_path = "", target_os="Windows", overwrite=True):
    if maxim_path == "": 
        print("Auto-detecting MaximSDK...")
        # Check environment variable
        if "MAXIM_PATH" in os.environ.keys():
            print("Checking MAXIM_PATH environment variable..")
            maxim_path = os.environ["MAXIM_PATH"]
        # Check default install locations
        elif "Windows" in platform.platform() and os.path.exists("C:/MaximSDK"):
            print("Checking default Windows location...")
            maxim_path = "C:/MaximSDK"
        else:
            print("Failed to auto-locate the MaximSDK...  set maxim_path in function call and try again.")
            return False

    # Search for list of targets
    targets = []
    for dir in os.scandir(os.path.join(maxim_path, "Examples")):
        targets.append(dir.name)
    

    for target in targets:

        # For this target, get the list of supported boards.
        boards = []
        for dir, subdirs, files in os.walk(os.path.join(maxim_path, "Libraries", "Boards", target)):
            if "board.mk" in files: 
                boards.append(os.path.split(dir)[1])

        # Set default board.  Try EvKit_V1, otherwise use first entry in list
        board = "EvKit_V1"
        if board not in boards: board = boards[0]

        for dir, subdirs, files in os.walk(os.path.join(maxim_path, "Examples", target)):
            if "Makefile" in files:
                if ".vscode" not in subdirs or (".vscode" in subdirs and overwrite):
                    if target_os == "Windows":
                        create_project(dir, target, board)
                    elif target_os == "Linux":
                        create_project(dir, target, board, M4_OCD_target_file=f"{str.lower(target)}.cfg")
    
if __name__ == "__main__":
    generate_maximsdk(maxim_path="C:/Users/Jake.Carter/repos/fork/MAX78000_SDK", target_os="Linux")