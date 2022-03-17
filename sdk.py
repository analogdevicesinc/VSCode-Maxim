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
*******************************************************************************
*/
"""

from dataclasses import dataclass
from typing import Generator
from utils import *
import json
import jsonpickle
import re
from copy import *

def get_baseitems(g: Generator):
    """
    Get a list of items inside of a generator.  Returns base string names only, ie. "myfile.txt" or "Examples" for a directory.

    Used to simplify searching for sub-items so that statements like "if i in get_baseitems(some generator/list of paths): ..." can be written more easily
    """
    return list(map(lambda i: i.name, g))

@dataclass
class Target():
    name: str
    boards: list
    
@dataclass
class Adapter():
    name: str
    cfg_file: Path

@dataclass
class Board():
    name: str
    target: Target
    adapters: list

@dataclass 
class Library():
    name: str
    path: Path
    ipaths: tuple
    vpaths: tuple
    whitelist: bool
    targets: tuple

    def from_libinfo(filepath):
        """
        Returns a Library instance instantiated from a json info file
        """
        filepath = Path(filepath)
        with open(filepath, "r") as f:
            libinfo = json.load(f)
            keys = libinfo.keys()
            assert "name" in keys and "ipaths" in keys and "vpaths" in keys and "whitelist" in keys, f"{filepath} Bad libinfo.json file!"

            _name = libinfo["name"]
            _path = filepath.parent
            _ipaths = tuple(i for i in libinfo["ipaths"])
            _vpaths = tuple(i for i in libinfo["vpaths"])
            _whitelist = libinfo["whitelist"]
            _targets = tuple(i for i in libinfo["targets"]) if "targets" in keys else None

            return Library(
                _name,
                _path,
                _ipaths,
                _vpaths,
                _whitelist,
                _targets
            )

    def get_ipaths(self, target=None):
        """
        Returns a tuple of include paths for the library.  
        If "target" is specified, the return generator will include paths specific to that target in addition to the common paths.
        If the library is whitelisted (Library.whitelist is True), "target" is specified, and there is no matching
        entry in the library, this function will return an empty tuple.
        """
        target_info = None

        if self.whitelist is True and target is None:
            return () # Return empty tuple
        else:
            _ipaths = list(map(lambda p: self.path.joinpath(p), self.ipaths)) # Common paths

            if target is not None and self.targets is not None:  # Search for match  
                for i in self.targets:
                    if ("name" in i.keys() and i["name"] == target):
                        target_info = i
        
            if target_info is not None and "ipaths" in target_info.keys():
                _ipaths += list(map(lambda p: self.path.joinpath(p), target_info["ipaths"])) # Target-specific paths

        return tuple(_ipaths)

    def get_hfiles(self, target=None):
        hfiles = []
        for ipath in self.get_ipaths(target):
            hfiles += ipath.rglob("*.h")
        return tuple(get_baseitems(hfiles))

    def get_vpaths(self, target: str):
        """
        Returns a tuple of browse paths for the library.  
        If "target" is specified, the return generator will include paths specific to that target in addition to the common paths.
        If the library is whitelisted (Library.whitelist is True), "target" is specified, and there is no matching
        entry in the library, this function will return an empty tuple.
        """
        target_info = None

        if self.whitelist is True and target is None:
            return () # Return empty tuple
        else:
            _vpaths = list(map(lambda p: self.path.joinpath(p), self.vpaths)) # Common paths

            if target is not None and self.targets is not None:  # Search for match  
                for i in self.targets:
                    if ("name" in i.keys() and i["name"] == target):
                        target_info = i
        
            if target_info is not None and "vpaths" in target_info.keys():
                _vpaths += list(map(lambda p: self.path.joinpath(p), target_info["vpaths"])) # Target-specific paths

        return tuple(_vpaths)

    def get_vfiles(self, target):
        vfiles = []
        for vpath in self.get_vpaths(target):
            vfiles += vpath.rglob("*.c")
        return tuple(get_baseitems(vfiles))

@dataclass
class Example():
    name: str
    path: Path
    target: Target
    riscv: False
    boards: list
    hfiles: list
    libs: list

class SDK():
    @time_me
    def __init__(self, maxim_path):
        # Populate initial info
        self.maxim_path = Path(maxim_path).absolute()
        (targets, boards) = get_targets_and_boards(self.maxim_path)
        self.targets = targets
        self.boards = boards
        self.libs = get_libraries(self.maxim_path)
        self.examples = get_examples(self.maxim_path, targets)

        # Match examples to libraries
        for e in self.examples:
            for l in self.libs:
                lib_hfiles = l.get_hfiles(e.target.name)
                for hfile in e.hfiles:
                    if hfile in lib_hfiles and l not in e.libs:
                        e.libs.append(l)

    def freeze(self, filename):
        with open(filename, "w+") as f:
            f.write(json.dumps(jsonpickle.encode(self)))

    def thaw(self, filename):
        with open(filename, "r") as f:
            tmp = jsonpickle.decode(json.load(f))
            self.maxim_path = tmp.maxim_path
            self.targets = tmp.targets
            self.boards = tmp.boards
            self.libs = tmp.libs
            self.examples = tmp.examples

@time_me
def get_targets_and_boards(maxim_path):
    maxim_path = Path(maxim_path).absolute()
    boards_dir = maxim_path.joinpath("Libraries", "Boards")

    # Detect targets and their supported boards
    targets = []
    boards = []
    for target_dir in boards_dir.iterdir():
        t = Target(target_dir.name, [])

        board_dirs = list(target_dir.iterdir())
        if target_dir.joinpath("Include").exists(): board_dirs.remove(target_dir.joinpath("Include"))
        if target_dir.joinpath("Source").exists(): board_dirs.remove(target_dir.joinpath("Source"))
            
        for board_dir in board_dirs:
            b = Board(board_dir.name, t, [])
            adapterinfo_file = board_dir.joinpath("adapterinfo.json")
            if adapterinfo_file.exists():
                with open(adapterinfo_file) as f:
                    adapterinfo = json.load(f)
                    for a in adapterinfo: b.adapters.append(Adapter(a["name"], a["cfg_file"]))

            t.boards.append(b)
            boards.append(b)

        targets.append(t)

    return (targets, boards)

@time_me
def get_examples(maxim_path, targets: list):
    maxim_path = Path(maxim_path).absolute()
    examples_dir = maxim_path.joinpath("Examples")

    # Locate examples for each target
    examples = []
    for t in targets:
        assert type(t) is Target
        for Makefile in examples_dir.joinpath(t.name).rglob("Makefile"):
            e = Example(
                    Makefile.parent.name,
                    Makefile.parent,
                    t,
                    "Makefile.RISCV" in get_baseitems(Makefile.parent.iterdir()),
                    [], # Filling these in later...
                    [],
                    []
                )

            exampleinfo_file = Makefile.parent.joinpath("exampleinfo.json")
            
            if exampleinfo_file.exists():
                with open(exampleinfo_file):
                    exampleinfo = json.load(exampleinfo_file)
                    e.boards = t.boards if exampleinfo["boards"] == "all" else exampleinfo["boards"]

            # Get all non-standard header files used in the example source code
            for cfile in e.path.rglob("*.c"):
                hfiles = get_hfiles(cfile)
                for hfile in hfiles:
                    if hfile not in e.hfiles:
                        e.hfiles.append(hfile)

            examples.append(e)

    return tuple(examples)

def get_hfiles(filepath):
    hfiles = []
    try:
        with open(filepath, "r") as c:
            lines = c.readlines()
            for l in lines: 
                if "#include" in l:
                    # Search for non-standard #includes - ie. #include "myheader.h"
                    # [\"] means character matching "
                    # \S+ is equivalent to %s in scanf
                    # Use raw string as recommended by Python docs (r"...")
                    m = re.search(r"[\"]\S+.h[\"]", l)
                    if m is not None:
                        mstring = l[m.start() + 1:m.end() - 1] # strip quotes
                        if mstring not in hfiles: hfiles.append(mstring)
    except:
        print(f"Failed to get header files from {filepath}")

    return tuple(hfiles)

@time_me
def get_libraries(maxim_path):
    maxim_path = Path(maxim_path).absolute()
    libs_path = maxim_path.joinpath("Libraries")

    libs = []

    for lib_path in libs_path.iterdir():
        info_file = lib_path.joinpath("libinfo.json")
        if info_file.exists():
            libs.append(Library.from_libinfo(info_file))

    return tuple(libs)