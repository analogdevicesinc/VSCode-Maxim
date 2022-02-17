from dataclasses import dataclass
import json
from dataclasses import dataclass
from pathlib import Path

def parse_json(filename):
    """
    Parse values from a json file into a template-friendly (all-caps keys) dictionary
    """
    f = open(filename, "r")
    d = json.load(f)

    # Convert key values to uppercase for easier template parsing
    keys = list(d.keys()) # Keys are changing on the fly, so can't use a view object
    for k in keys:
        d[k.upper()] = d.pop(k)
    
    return d

# Timer wrapper function
import time
def time_me(f):

    def wrapper(*args, **kwargs):
        start = time.time() # Start timer
        res = f(*args, **kwargs)
        end = time.time() # Stop timer
        duration = end - start # Calculate duration
        print(f"{f.__name__} took {duration}s") # Print timer info
        
        return res

    return wrapper