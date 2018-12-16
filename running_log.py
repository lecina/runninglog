from all_runs import all_runs
from utilities import utilities
from constants import constants
from reader import reader

import os.path
import json

class RunningLog():
    def __init__(self):
        self.allRuns = all_runs.AllRuns()

        self.output_dir = "../running_log_data/"
        self.raw_json_output_dir = os.path.join(self.output_dir, "raw")

    def load_files_in_directory(self, directory):
        loaded_files = self.allRuns.load_files_in_dir(directory)
        return loaded_files


    def generate_empty_json(self):
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

    def load_files_to_load(self):
        directory = constants.TO_LOAD_FOLDER
        loaded_files = self.load_files_in_directory(directory)

        utilities.make_dir(self.raw_json_output_dir)
        for (fname, date) in loaded_files:
            output_dir = os.path.join(self.raw_json_output_dir, str(date.year))
            utilities.make_dir(output_dir)
            output_fname = str(date.month) + ".json"
            oname = os.path.join(output_dir, output_fname)

            #append if exists
            if os.path.isfile(oname):
                #jsonFile = open(fname, 'r').read()
                jsonFile = reader.read_file(fname)
                outputJsonFile = reader.read_file(oname)
                outputJsonFileList = outputJsonFile[constants.blockNames.FileParams.list]
                if jsonFile in outputJsonFileList:
                    print "Json has already been inserted!"
                else:
                    outputJsonFileList.append(jsonFile)
                    #Better write and if correct, replace
                    with open(oname, "w") as json_file:
                        json_file.write(json.dumps(outputJsonFile, indent=4, separators=(',', ' : ')))
            #create if doesn't
            else:
                jsonFile = reader.read_file(fname)
                newdict = {}
                newdict[constants.blockNames.FileParams.list] = [jsonFile]
                with open(oname, "w") as json_file:
                    json_file.write(json.dumps(newdict, indent=4, separators=(',', ' : ')))
                print "Wrote new file:", oname


def main():
    allRuns = all_runs.AllRuns()

if __name__ == "__main__":
    main()
