import os
from subprocess import run
import platform
import time

def log(string, file):
    print(string)
    file.write(f"{string}\n")
    file.flush()

def timestamp():
    now = time.localtime()
    return f"[{now.tm_mon}/{now.tm_mday}/{now.tm_year} {now.tm_hour}:{now.tm_min}:{now.tm_sec}]"

duration = 0
def time_me(f):

    def wrapper(*args, **kwargs):
        start = time.time() # Start timer
        res = f(*args, **kwargs)
        end = time.time() # Stop timer
        global duration
        duration = end - start # Calculate duration
        
        return res

    return wrapper

@time_me
def ps(cmd, env=None):
    # Windows
    # if env is None:
    #     result = run(["powershell", cmd], capture_output=True)
    
    # else:
    #     result = run(["powershell", cmd], env=env, capture_output=True)

    # Linux
    if env is None: result = run(cmd, capture_output=True, shell=True)
    else: result = run(cmd, env=env, capture_output=True, shell=True)

    return result

def sync_examples():
    # Inject .vscode folder into example projects
    print("Inject .vscode folder into example projects...")
    ps("Copy-Item ./MaximLP/Inject/* ./MaximLP/New_Project/ -force -Recurse")
    ps("Copy-Item ./MaximSDK/Inject/* ./MaximSDK/New_Project/ -force -Recurse")

def release(version):
    r_dir = f"./Releases/VSCode-Maxim-{version}" # Release directory

    # Create release release directory
    print("Creating release directory...")
    ps(f"New-Item -Path {r_dir} -ItemType Directory")        

    sync_examples()

    # Package release
    print("Packaging...")
    ps(f"New-Item -Path {r_dir}/MaximLP -ItemType Directory")
    ps(f"Copy-Item ./MaximLP/* {r_dir}/MaximLP/ -force -Recurse")

    ps(f"New-Item -Path {r_dir}/MaximSDK -ItemType Directory")
    ps(f"Copy-Item ./MaximSDK/* {r_dir}/MaximSDK/ -force -Recurse")

    ps(f"Copy-Item ./readme.md {r_dir}/ -force")
    ps(f"Copy-Item ./userguide.md {r_dir}/ -force")
    ps(f"Copy-Item ./LICENSE.txt {r_dir}/ -force")

    #Archive release
    print("Archiving...")
    ps(f"compress-archive -path {r_dir} -DestinationPath {r_dir}/VSCode-Maxim-{version}")

    # Clean up
    print("Cleaning up...")
    ps(f"Remove-Item {r_dir}/readme.md")
    ps(f"Remove-Item {r_dir}/userguide.md")
    ps(f"Remove-Item {r_dir}/LICENSE.txt")
    ps(f"Remove-Item {r_dir}/MaximLP -Recurse")
    ps(f"Remove-Item {r_dir}/MaximSDK -Recurse")

    print("Done!")

# Tests cleaning and compiling example projects for target platforms.  If no targets, boards, projects, etc. are specified then it will auto-detect
def test(targets=None, boards=None, projects=None):
    env = os.environ.copy()
    curplatform = platform.system()

    # Simulate the VS Code terminal by appending to the Path
    MAXIM_PATH = ""
    if curplatform == 'Linux':
        MAXIM_PATH = "/home/jcarter/MaximSDK" # Linux
        env["PATH"] = f"{MAXIM_PATH}/Tools/OpenOCD:/{MAXIM_PATH}/Tools/GNUTools/bin:{MAXIM_PATH}/Tools/xPack/riscv-none-embed-gcc/bin:" + env["PATH"] # Linux
    elif curplatform == 'Windows':
        MAXIM_PATH = "C:/MaximSDK" # Windows
        env["PATH"] = f"{MAXIM_PATH}/Tools/MinGW/msys/1.0/bin;{MAXIM_PATH}/Tools/OpenOCD;{MAXIM_PATH}/Tools/GNUTools/bin;{MAXIM_PATH}/Tools/xPack/riscv-none-embed-gcc/bin;" + env["PATH"] # Windows
    
    LOG_DIR = os.getcwd()

    # Create log file
    try: os.mkdir(f"{LOG_DIR}/buildlogs")
    except FileExistsError: pass
    logfile = open(f"{LOG_DIR}/test.log", 'w')
    
    # Log system info
    log(timestamp(), logfile)
    log(f"[PLATFORM] {platform.platform()}", logfile)

    # Get list of target micros if none is specified
    if targets is None:
        targets = []

        for dir in os.scandir(f"{MAXIM_PATH}/Examples"):
            targets.append(dir.name) # Append subdirectories of Examples to list of target micros

        log(f"[TARGETS] Detected targets {targets}", logfile)
    
    else:
        assert(type(targets) is list)
        log(f"[TARGETS] Testing {targets}", logfile)

    # Enforce alphabetical ordering
    targets = sorted(targets)

    # Create subfolders for target-specific logfiles
    for t in targets: 
        try: os.mkdir(f"{LOG_DIR}/buildlogs/{t}")
        except FileExistsError: pass

    # Track failed projects for end summary
    failed = []
    count = 0

    for target in targets:
        log("====================", logfile)
        log(f"[TARGET] {target}", logfile)

        # Get list of supported boards for this target.
        if boards is None:
            boards = []
            for dirpath, subdirs, items in os.walk(f"{MAXIM_PATH}/Libraries/Boards/{target}"):
                if "board.mk" in items and curplatform == 'Linux': boards.append(dirpath.split('/')[-1]) # Linux
                elif "board.mk" in items and curplatform == 'Windows': boards.append(dirpath.split('\\')[-1]) # Board string will be the last folder in the directory path # Windows

            log(f"[BOARDS] Detected {boards}", logfile)

        else:
            assert(type(boards) is list)
            log(f"[BOARDS] Testing {boards}")

        boards = sorted(boards) # Enforce alphabetical ordering
                
        # Get list of examples for this target.  If a Makefile is in the root directory it's an example.
        if projects is None:
            projects = []
            for dirpath, subdirs, items in os.walk(f"{MAXIM_PATH}/Examples/{target}"):
                if 'Makefile' in items:
                    projects.append(dirpath)  

            log(f"[PROJECTS] Detected {projects}", logfile)

        else:
            assert(type(projects) is list)
            log(f"[PROJECTS] Testing {projects}")

        projects = sorted(projects) # Enforce alphabetical ordering

        # Test each project
        for project in projects:
            if curplatform == 'Linux': project_stripped = project.split('/')[-1] # Linux
            elif curplatform == 'Windows': project_stripped = project.split('\\')[-1] # Windows

            log("---------------------", logfile)
            log(f"[{target}]\t[{project_stripped}]", logfile)
            os.chdir(project) # Need to us os.chdir to set working directory of subprocesses

            for board in boards:
                buildlog = f"{target}_{board}_{project_stripped}.log"
                success = True

                # Test build (make all)
                build_cmd = f"make all TARGET={target} MAXIM_PATH={MAXIM_PATH} BOARD={board} MAKE=make"
                res = ps(build_cmd, env=env) # Run build command

                # Error check build command
                if res.returncode != 0:
                    # Fail
                    success = False                    
                    log(f"{timestamp()}[{board}] --- [BUILD]\t[FAILED] Return code {res.returncode}.  See buildlogs/{buildlog}", logfile)            
                    
                    # Log detailed output to separate output file
                    with open(f"{LOG_DIR}/buildlogs/{target}/{buildlog}", 'w') as f:
                        f.write("===============\n")
                        f.write(timestamp() + '\n')
                        f.write(f"[PROJECT] {project}\n")
                        f.write(f"[BOARD] {board}\n")
                        f.write(f"[BUILD COMMAND] {build_cmd}\n")
                        f.write("===============\n")
                        for line in str(res.stdout + res.stderr, encoding="ASCII").splitlines():
                            f.write(line + '\n')

                else: log(f"{timestamp()}[{board}] --- [BUILD]\t[SUCCESS] {round(duration, 4)}s", logfile)                

                # Test clean (make clean)
                clean_cmd = f"make clean TARGET={target} MAXIM_PATH={MAXIM_PATH} BOARD={board} MAKE=make"
                res = ps(clean_cmd, env=env) # Run clean command

                # Error check clean command
                if res.returncode != 0:
                    log(f"{timestamp()}[{board}] --- [CLEAN]\t[SUCCESS] {str(res.stderr, encoding='ASCII')}", logfile)
                    success = False
                else: log(f"{timestamp()}[{board}] --- [CLEAN]\t[SUCCESS] {round(duration, 4)}s", logfile)

                # Add any failed projects to running list
                project_info = {
                    "target":target,
                    "project":project_stripped,
                    "board":board,
                    "path":project,
                    "logfile":f"buildlogs/{buildlog}"
                    }
                if not success and project_info not in failed: failed.append(project_info)
                count += 1

        log("====================", logfile)

    log(f"[SUMMARY] Tested {count} projects.  {count - len(failed)}/{count} succeeded.  Failed projects: ", logfile)
    for pinfo in failed:
        log(f"[{pinfo['target']}] {pinfo['project']} for {pinfo['board']}...  see {pinfo['logfile']}", logfile)

if __name__ == "__main__":
    test(targets=["MAX78000"])