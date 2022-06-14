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