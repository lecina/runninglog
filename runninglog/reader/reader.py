import json
import sys

def __unicodeToStr(data):
    #convert dict
    if isinstance(data, dict):
        return { __unicodeToStr(key): __unicodeToStr(value) for key, value in data.iteritems() }
    #convert list
    if isinstance(data, list):
        return [ __unicodeToStr(val) for val in data ]
    #convert unicode to str
    if isinstance(data, unicode):
        return data.encode('utf-8')

    return data

def read_file(jsonParams):
    jsonFile = open(jsonParams, 'r').read()
    try:
        parsedJSON = json.loads(jsonFile)
    except ValueError:
        sys.exit("Could not read: %s"%jsonParams)
    return parsedJSON
