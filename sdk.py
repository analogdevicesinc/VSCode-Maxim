from dataclasses import dataclass
from typing import Generator
from utils import *
import json

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
class Example():
    name: str
    path: Path
    target: Target
    riscv: False
    boards: list

class SDK():
    def __init__(self, maxim_path):
        (targets, boards) = get_targets_and_boards(maxim_path)
        self.targets = targets
        self.boards = boards
        self.examples = get_examples(maxim_path, targets)

def get_baseitems(g: Generator):
    """
    Get a list of items inside of a generator.  Returns base string names only, ie. "myfile.txt" or "Examples" for a directory.

    Used to simplify searching for sub-items so that statements like "if i in get_baseitems(some generator/list of paths): ..." can be written more easily
    """
    return list(map(lambda i: i.name, g))

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
        board_dirs.remove(target_dir.joinpath("Include"))
        board_dirs.remove(target_dir.joinpath("Source"))
            
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
                    True if "Makefile.RISCV" in get_baseitems(Makefile.parent.iterdir()) else False,
                    None
                )

            exampleinfo_file = Makefile.parent.joinpath("exampleinfo.json")
            
            if exampleinfo_file.exists():
                with open(exampleinfo_file):
                    exampleinfo = json.load(exampleinfo_file)
                    e.boards = t.boards if exampleinfo["boards"] == "all" else exampleinfo["boards"]

            examples.append(e)

    return examples