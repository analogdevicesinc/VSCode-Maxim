import json

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