import os
import shutil

defaults = {
    "MAXIM_PATH":"C:/MaximSDK", 
    "PROGRAM_FILE":"${config:project_name}.elf",
    "SYMBOL_FILE":"${config:program_file}",
    "M4_OCD_INTERFACE_FILE":"cmsis-dap.cfg",
    "M4_OCD_TARGET_FILE":"${config:target}.cfg",
    "RV_OCD_INTERFACE_FILE":"ftdi/olimex-arm-usb-ocd-h.cfg",
    "RV_OCD_TARGET_FILE":"${config:target}-riscv.cfg"
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
    defines: list = [],
    i_paths: list = [],
    v_paths: list = [],
):

    template_dir = os.path.join("MaximSDK", "Template")  # Where to find the VS Code template directory
    template_prefix = "template"  # Filenames beginning with this will have substitution

    tmp = []  # Work-horse list, linter be nice
    if defines is not None:
        # Parse defines...
        # ---
        tmp = defines
        tmp = list(map(lambda s: s.strip("-D"), tmp))  # VS Code doesn't want -D
        tmp = list(map("\"{0}\"".format, tmp))  # Surround with quotes
        defines_parsed = ",\n\t\t\t\t".join(tmp)  # csv, newline, and tab alignment
        # ---

    # Parse include paths...
    tmp = i_paths
    tmp = list(map("\"{0}\"".format, tmp))  # Surround with quotes
    i_paths_parsed = ",\n\t\t\t\t".join(tmp)  # csv, newline, and tab alignment

    # Parse browse paths...
    tmp = v_paths  # Space-separated
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
                            replace("\"##__ADDITIONAL_INCLUDES__##\"", i_paths_parsed).
                            replace("\"##__DEFINES__##\"", defines_parsed).
                            replace("\"##__ADDITIONAL_SOURCES__##\"", v_paths_parsed)
                        )

            else:
                # There is a non-template file to copy
                shutil.copy(os.path.join(directory, file), out_path)
                
