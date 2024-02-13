###############################################################################
 #
 # Copyright (C) 2022-2023 Maxim Integrated Products, Inc. All Rights Reserved.
 # (now owned by Analog Devices, Inc.),
 # Copyright (C) 2023 Analog Devices, Inc. All Rights Reserved. This software
 # is proprietary to Analog Devices, Inc. and its licensors.
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #     http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 #
 ##############################################################################

from collections.abc import MutableMapping
import json
from pathlib import Path
import hashlib
import os

class UpperDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.d = dict()
        self.update(dict(*args, **kwargs))

    def _parse_key(self, key):
        return str(key).upper().replace(".", "_")

    def __setitem__(self, key, value) -> None:
        self.d[self._parse_key(key)] = value

    def __getitem__(self, key):
        return self.d[self._parse_key(key)]

    def __delitem__(self, key) -> None:
        del self.d[self._parse_key(key)]

    def __iter__(self):
        return iter(self.d)

    def __len__(self):
        return len(self.d)

def parse_json(filename):
    """
    Parse values from a json file into a template-friendly (all-caps keys) dictionary
    """
    f = open(filename, "r")
    d = json.load(f)
    return UpperDict(d)

# Timer wrapper function
import time
def time_me(f):

    def wrapper(*args, **kwargs):
        start = time.time() # Start timer
        res = f(*args, **kwargs)
        end = time.time() # Stop timer
        duration = end - start # Calculate duration
        print(f"{f} took {duration}s") # Print timer info
        
        return res

    return wrapper

def hash(val):
    if not isinstance(val, bytes):
        val = bytes(val, encoding="utf-8")
    return hashlib.sha1(val).digest()

def hash_file(filepath):
    return hash(open(Path(filepath), 'rb').read())

def hash_folder(folderpath) -> bytes:
    folderpath = Path(folderpath)
    result = b''
    for dir, subdirs, files in os.walk(folderpath):
        for f in sorted(files):
            file_path = Path(dir).joinpath(f)
            relative_path = file_path.relative_to(folderpath)

            result = hash(result + hash_file(file_path) + bytes(str(relative_path), encoding="utf-8"))
            
    return result

def compare_content(content: str, file: Path) -> bool:
    """
    Compare the 'content' string to the existing content in 'file'.

    It seems that when a file gets written there may be some metadata that is affecting
    the hash functions.  As a result, this function writes 'content' to a temporary file,
    then checks for equality using the temp file.
    """
    if not file.exists():
        return False

    tmp = file.parent.joinpath("tmp")
    with open(tmp, "w", encoding='utf-8') as f:
        f.write(content)

    match = (hash_file(file) == hash_file(tmp))
    os.remove(tmp)
    return match