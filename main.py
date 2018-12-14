from reader import reader
from single_run import single_run
from constants import constants, blockNames
from utilities import utilities

import os.path
import glob

def load_single_run(filename):
    parsed_json = reader.read_file(filename)
    singleRun = single_run.SingleRun()
    singleRun.load_json(parsed_json)
    return singleRun

def generate_empty_json():

    fname_template = os.path.join(constants.TO_LOAD_FOLDER,
                                constants.JSON_TEMPLATE_OUTPUT_NAME)
    fname = fname_template%"" 
    i=1
    while os.path.isfile(fname):
        suffix = "_%d"%i
        fname = fname_template%suffix
        i += 1
        
    utilities.make_dir(constants.TO_LOAD_FOLDER)
    with open(fname, "w") as json_file:
        json_file.write(constants.EMPTY_JSON)

    print "Generated: %s"%fname

def load_files_to_load():
    wildcard = os.path.join(constants.TO_LOAD_FOLDER, '*')
    file_list = glob.glob(wildcard)

    if len(file_list) == 0:
        print "No files to read!"
        return

    for f in file_list:
        jsonFile = open(f, 'r').read()
        if jsonFile == constants.EMPTY_JSON:
            print "Empty json file: \"%s\"!\nCleaning it up!!"%f
            utilities.rm_file(f)
        else:
            #TODO: add json validator
            singleRun = load_single_run(f) 
            print singleRun
            print "=========="
            #TODO: do stuff

if __name__ == "__main__":
    singleRun = load_single_run("data/test.json")
