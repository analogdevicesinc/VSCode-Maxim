import os
from subprocess import run

def ps(cmd):
    result = run(["powershell", cmd], capture_output=True)
    if result.returncode != 0:
        print(result.stderr)

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

    #Archive release
    print("Archiving...")
    ps(f"compress-archive -path {r_dir} -DestinationPath {r_dir}/VSCode-Maxim-{version}")

    # Clean up
    print("Cleaning up...")
    ps(f"Remove-Item {r_dir}/readme.md")
    ps(f"Remove-Item {r_dir}/MaximLP -Recurse")
    ps(f"Remove-Item {r_dir}/MaximSDK -Recurse")

    print("Done!")

