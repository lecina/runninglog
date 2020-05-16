import os
import fnmatch
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

def read_file(json_filename):
    with open(json_filename, 'r') as json_file:
        json_str = json_file.read()

        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError as err:
            raise Exception(f"Could not read: {json_filename}; "
                            f"Error: {err}") from err
        except:
            raise Exception(f"Could not read: {json_filename}") from err

    return parsed_json

def get_json_files_in_subdirs(directory):
    """Get all JSON files in dir and subdirs

        Get all JSON files in root dir and subdirs

        Args:
            directory(str): Root directory

        Returns:
            list: List of JSON files
    """
    file_list = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.json'):
            file_list.append(os.path.join(root, filename))
    return file_list
