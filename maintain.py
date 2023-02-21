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

import os, sys
from subprocess import run
import platform
import time
import shutil
import argparse
from pathlib import Path
from datetime import date

# Get location of this file.
# Need to use this so that template look-ups are decoupled from the caller's working directory 
if getattr(sys, 'frozen', False):
    # https://pyinstaller.org/en/stable/runtime-information.html#run-time-information
    # Use sys.executable if app is bundled by pyinstaller
    here = Path(sys.executable).parent
    _vscode_dir = here.joinpath("VSCode")
else:
    here = Path(__file__).parent
    _vscode_dir = here

curplatform = platform.system() # Get OS

def log(string, file):
    with open(file, "a") as f:
        print(string)
        f.write(f"{string}\n")
        f.flush()

def timestamp():
    now = time.localtime()
    return f"[{now.tm_mon}/{now.tm_mday}/{now.tm_year} {now.tm_hour}:{now.tm_min}:{now.tm_sec}]"


duration = 0
def time_me(f):

    def wrapper(*args, **kwargs):
        start = time.time() # Start timer
        res = f(*args, **kwargs)
        end = time.time() # Stop timer
        global duration # Use global duration variable so main script can access elapsed time
        duration = end - start # Calculate duration
        
        return res

    return wrapper

@time_me
def run_cmd(*args, **kwargs):
    return run(*args, **kwargs)

def sync():
    # Inject .vscode folder into example projects
    inject_dir = _vscode_dir.joinpath("MaximSDK", "Inject", ".vscode")
    new_proj_dir = _vscode_dir.joinpath("MaximSDK", "New_Project", ".vscode")
    template_dir = _vscode_dir.joinpath("MaximSDK", "Template", ".vscode")

    # print("Syncing VSCode template...")
    for f in os.scandir(inject_dir):
        shutil.copy(f, new_proj_dir)

    # Copy files into template folder
    shutil.copy(inject_dir.joinpath("launch.json"), template_dir)
    shutil.copy(inject_dir.joinpath("c_cpp_properties.json"), template_dir)
    shutil.copy(inject_dir.joinpath("tasks.json"), template_dir)
    shutil.copy(inject_dir.joinpath("workaround.h"), template_dir)
    shutil.copy(inject_dir.joinpath("flash.gdb"), template_dir)
    shutil.copy(_vscode_dir.joinpath("README.md"), template_dir)

def release(version):
    sync()
    
    r_dir = Path(f"./Releases/VSCode-Maxim-{version}") # Release directory

    # maxim_path = Path(maxim_path)
    # vscode_folders = maxim_path.rglob("*/.vscode")
    # for i in vscode_folders:
    #     print(f"Copying {i}")
    #     out_dir = r_dir.joinpath(Path(str(i).replace(i.anchor, ""))) # Strip drive info and pre-pend output directory
    #     shutil.copytree(i, out_dir, dirs_exist_ok=True)

    print("Copying Inject & New_Project folders")
    shutil.copytree(Path("MaximSDK/Inject"), r_dir.joinpath("Inject"), dirs_exist_ok=True)
    shutil.copytree(Path("MaximSDK/New_Project"), r_dir.joinpath("New_Project"), dirs_exist_ok=True)

    print("Copying markdown files")
    shutil.copy("README.md", r_dir)
    shutil.copy("userguide.md", r_dir)
    shutil.copy("LICENSE.md", r_dir)

    # Copy in to installer package
    print("Updating installer package...")
    shutil.copytree(r_dir, Path("./installer/com.maximintegrated.dist.vscodemaxim/data/Tools/VSCode-Maxim"), dirs_exist_ok=True)

    # Update version # and release date in package.xml
    # ---
    today = date.today()
    lines = []
    package_path = Path("installer/com.maximintegrated.dist.vscodemaxim/meta/package.xml")
    with open(package_path, "r") as xml:
        lines = xml.readlines()
        for i in range(len(lines)):
            if "<Version>" in lines[i]:
                lines[i] = f"    <Version>{version[1]}.{version[2]}.{version[3]}</Version>\n"

            elif "<ReleaseDate>" in lines[i]:
                lines[i] = f"    <ReleaseDate>{today.isoformat()}</ReleaseDate>\n"

    
    with open(package_path, "w") as xml:
        xml.writelines(lines)

    # ---
    
    # Update tag in installscript.js
    installscript_path = Path("installer/com.maximintegrated.dist.vscodemaxim/meta/installscript.js")
    with open(installscript_path, "r") as js:
        lines = js.readlines()
        for i in range(len(lines)):
            if "var tag =" in lines[i]:
                lines[i] = f"    var tag = \"v{version[1]}.{version[2]}.{version[3]}\";\n"

    with open(installscript_path, "w") as js:
        js.writelines(lines)

    # Update dat afolder in installer package
    shutil.copytree(r_dir, Path("installer/com.maximintegrated.dist.vscodemaxim/data/Tools/VSCode-Maxim/"), dirs_exist_ok=True)

    # Update release date
    print("Done!")

# Tests cleaning and compiling example projects for target platforms.  If no targets, boards, projects, etc. are specified then it will auto-detect
def test(maxim_path, targets=None, boards=None, projects=None):
    maxim_path = Path(maxim_path).resolve()
    env = os.environ.copy()

    # Simulate the VS Code terminal by appending to the Path
    # if curplatform == 'Linux':
    #     env["PATH"] = f"{maxim_path.as_posix()}/Tools/GNUTools/10.3/bin:{maxim_path.as_posix()}/Tools/xPack/riscv-none-embed-gcc/10.2.0-1.2/bin:" + env["PATH"]
    # elif curplatform == 'Windows':
    #     env["PATH"] = f"{maxim_path.as_posix()}/Tools/GNUTools/10.3/bin;{maxim_path.as_posix()}/Tools/xPack/riscv-none-embed-gcc/10.2.0-1.2/bin;{maxim_path.as_posix()}/Tools/MSYS2/usr/bin;" + env["PATH"]
    
    log_dir = Path(os.getcwd()).joinpath("buildlogs")

    # Create log file
    if not log_dir.exists():
        os.mkdir(log_dir)
    logfile = log_dir.joinpath("test.log")
    
    # Log system info
    log(timestamp(), logfile)
    log(f"[PLATFORM] {platform.platform()}", logfile)
    log(f"[MAXIM_PATH] {maxim_path}", logfile)

    # Get list of target micros if none is specified
    if targets is None:
        targets = []

        for dir in os.scandir(f"{maxim_path}/Examples"):
            targets.append(dir.name) # Append subdirectories of Examples to list of target micros

        log(f"[TARGETS] Detected targets {targets}", logfile)
    
    else:
        assert(type(targets) is list)
        log(f"[TARGETS] Testing {targets}", logfile)

    # Enforce alphabetical ordering
    targets = sorted(targets)

    # Create subfolders for target-specific logfiles
    for t in targets:
        sub_dir = log_dir.joinpath(t)
        if not sub_dir.exists():
            os.mkdir(sub_dir)

    # Track failed projects for end summary
    failed = []
    count = 0

    for target in targets:
        log("====================", logfile)
        log(f"[TARGET] {target}", logfile)

        # Get list of supported boards for this target.
        if boards is None:
            boards = []
            for dirpath, subdirs, items in os.walk(maxim_path.joinpath("Libraries", "Boards", target)):
                if "board.mk" in items:
                    boards.append(Path(dirpath).name)

            log(f"[BOARDS] Detected {boards}", logfile)

        else:
            assert(type(boards) is list)
            log(f"[BOARDS] Testing {boards}", logfile)

        boards = sorted(boards) # Enforce alphabetical ordering
                
        # Get list of examples for this target.  If a Makefile is in the root directory it's an example.
        if projects is None:
            projects = []
            for dirpath, subdirs, items in os.walk(maxim_path.joinpath("Examples", target)):
                if 'Makefile' in items and ("main.c" in items or "project.mk" in items):
                    projects.append(Path(dirpath)) 

            log(f"[PROJECTS] Detected {projects}", logfile)

        else:
            assert(type(projects) is list)
            log(f"[PROJECTS] Testing {projects}", logfile)

        projects = sorted(projects) # Enforce alphabetical ordering

        # Test each project
        for project in projects:
            project_name = project.name
            print(project_name)

            log("---------------------", logfile)
            log(f"[{target}]\t[{project_name}]", logfile)

            for board in boards:
                buildlog = f"{target}_{board}_{project_name}.log"
                success = True

                # Test build (make all)
                build_cmd = f"make -r -j 8 TARGET={target} MAXIM_PATH={maxim_path.as_posix()} BOARD={board} MAKE=make"
                res = run_cmd(build_cmd, env=env, cwd=project, shell=True, capture_output=True, encoding="utf-8") # Run build command

                # Error check build command
                if res.returncode != 0:
                    # Fail
                    success = False                    
                    log(f"{timestamp()}[{board}] --- [BUILD]\t[FAILED] Return code {res.returncode}.  See buildlogs/{buildlog}", logfile)            
                    
                    # Log detailed output to separate output file
                    with open(log_dir.joinpath(target, buildlog), 'w') as f:
                        f.write("===============\n")
                        f.write(timestamp() + '\n')
                        f.write(f"[PROJECT] {project}\n")
                        f.write(f"[BOARD] {board}\n")
                        f.write(f"[BUILD COMMAND] {build_cmd}\n")
                        f.write("===============\n")
                        f.write(res.stdout + res.stderr)

                else: log(f"{timestamp()}[{board}] --- [BUILD]\t[SUCCESS] {round(duration, 4)}s", logfile)                

                # Test clean (make clean)
                clean_cmd = f"make distclean TARGET={target} MAXIM_PATH={maxim_path} BOARD={board} MAKE=make"
                res = run_cmd(clean_cmd, env=env, cwd=project, shell=True, capture_output=True, encoding="utf-8") # Run clean command

                # Error check clean command
                if res.returncode != 0:
                    log(f"{timestamp()}[{board}] --- [CLEAN]\t[SUCCESS] {res.stderr}", logfile)
                    success = False
                else: log(f"{timestamp()}[{board}] --- [CLEAN]\t[SUCCESS] {round(duration, 4)}s", logfile)

                # Add any failed projects to running list
                project_info = {
                    "target":target,
                    "project":project_name,
                    "board":board,
                    "path":project,
                    "logfile":f"buildlogs/{buildlog}"
                    }
                if not success and project_info not in failed: failed.append(project_info)
                count += 1

        log("====================", logfile)
        boards = None # Reset boards list
        projects = None # Reset targets list

    log(f"[SUMMARY] Tested {count} projects.  {count - len(failed)}/{count} succeeded.  Failed projects: ", logfile)
    for pinfo in failed:
        log(f"[{pinfo['target']}] {pinfo['project']} for {pinfo['board']}...  see {pinfo['logfile']}", logfile)

parser = argparse.ArgumentParser("VSCode-Maxim maintainer utilities")
parser.add_argument("--maxim_path", type=str, help="(Optional) Location of the MaximSDK.  If this is not specified then the script will attempt to use the MAXIM_PATH environment variable.")

cmd_parser = parser.add_subparsers(dest="cmd", help="sub-command", required=True)

release_parser = cmd_parser.add_parser("release", help="Package a release")
release_parser.add_argument("version", type=str, help="Version # for the release")

sync_parser = cmd_parser.add_parser("sync", help="Sync all .vscode project folders")

test_parser = cmd_parser.add_parser("test", help="Run a build test of the SDK.")
test_parser.add_argument("--targets", type=str, nargs="+", required=False, help="Target microcontrollers to test.")
test_parser.add_argument("--boards", type=str, nargs="+", required=False, help="Boards to test.  Should match the BSP folder-name exactly.")
test_parser.add_argument("--projects", type=str, nargs="+", required=False, help="Examples to populate.  Should match the example's folder name.")

if __name__ == "__main__":
    args = parser.parse_args()

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

    if args.cmd == "release":
        release(args.version)
    
    elif args.cmd == "sync":
        sync()
    
    elif args.cmd == "test":
        test(args.maxim_path, targets=args.targets, boards=args.boards, projects=args.projects)
