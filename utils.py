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

from collections.abc import MutableMapping
from string import Template
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

class MSDKTemplate(Template):
    delimiter = "##__"

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