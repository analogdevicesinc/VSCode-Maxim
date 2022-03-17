import argparse
import platform
import os
from generate import *

parser = argparse.ArgumentParser(description="VSCode-Maxim command line tool.")

parser.add_argument("--os", type=str, choices=["Windows", "Linux"], help="(Optional) Operating system to generate the project files for.  If not specified the script will auto-detect.")
parser.add_argument("--maxim_path", type=str, help="(Optional) Location of the MaximSDK.  If this is not specified then the script will attempt to use the MAXIM_PATH environment variable.")

cmd_parser = parser.add_subparsers(dest="cmd", help="sub-command", required=True)

generate_parser = cmd_parser.add_parser("generate", help="Populate a MaximSDK installation's example projects with VS Code project files.")
generate_parser.add_argument("subcmd", choices=["SDK", "new"], help="What to generate.")

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
    if args.cmd == "generate":
        if args.subcmd == "SDK":
            print(f"Generating .vscode projects for all examples in SDK located at {args.maxim_path}")
            populate_maximsdk(target_os=args.os, maxim_path=args.maxim_path)
        elif args.subcmd == "new":
            pass
            # TODO: new project creator


    