import os
import fnmatch
import json
import sys

from runninglog.constants import constants

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

def get_files_in_subdirs(directory, extension):
    """Get all files in dir and subdirs that match extension

        Get all files in root dir and subdirs

        Args:
            directory(str): Root directory

        Returns:
            list: List of found files
    """
    file_list = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, extension):
            file_list.append(os.path.join(root, filename))
    return file_list

def read_json_file(filename):
    """Read JSON file

        Read JSON file as dictionary

        Args:
            filename(str): Filename

        Returns:
            dict: Dictionary with file content
    """
    with open(filename, 'r') as json_file:
        json_str = json_file.read()

        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError as err:
            raise Exception(f"Could not read: {json_filename}; "
                            f"Error: {err}") from err
        except:
            raise Exception(f"Could not read: {json_filename}") from err

    return parsed_json


def get_json_runs_in_subdirs(directory, verbose=False):
    file_list = get_files_in_subdirs(directory, '*.json')

    read_runs = []
    for filename in file_list:
        if verbose:
            print ("Reading", filename)

        parsed_json = read_json_file(filename)

        #Omit empty JSON or files
        if parsed_json != constants.EMPTY_JSON and parsed_json != "":
            read_runs.append(parsed_json)

    return read_runs
