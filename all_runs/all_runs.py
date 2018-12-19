from reader import reader
from single_run import single_run
from constants import constants, blockNames
from utilities import utilities

import os
import fnmatch
import pandas as pd
import pickle

class AllRuns():
    def __init__(self):
        self.df = pd.DataFrame()

    def read_single_run(self, filename):
        print "Reading", filename
        #TODO: raise/catch exception
        parsed_json = reader.read_file(filename)

        if blockNames.FileParams.list in parsed_json.keys():
            singleRuns = []
            for json_dir in parsed_json[blockNames.FileParams.list]:
                singleRun = single_run.SingleRun()
                singleRun.load_json(json_dir)
                singleRuns.append(singleRun)
            return singleRuns
        else:
            singleRun = single_run.SingleRun()
            singleRun.load_json(parsed_json)
            return singleRun

    def load_files_in_dir(self, directory):
        file_list = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.json'):
                file_list.append(os.path.join(root, filename))

        if len(file_list) == 0:
            print "No files to read!"
            return

        parsed_json_files = []
        for f in file_list:
            jsonFile = open(f, 'r').read()
            if jsonFile == constants.EMPTY_JSON:
                print "Empty json file: \"%s\"!\nCleaning it up!!"%f
                utilities.rm_file(f)
            else:
                #TODO: add json validator
                srs = self.read_single_run(f) 
                if type(srs) is not list:
                    srs = [srs]
                
                for sr in srs:
                    sr_ds = pd.Series(sr.as_dict())
                
                    if self.df.size == 0:
                        already_added = False
                    else:
                        already_added = sum((self.df.values==sr_ds.values).all(axis=1))

                    if already_added:
                        print "Not adding already added move:", f
                    else:
                        self.df = self.df.append(sr_ds, ignore_index=True)
                        parsed_json_files.append((f,sr.date))

        return parsed_json_files

    def save_all_runs(self, fname):
        self.df.to_pickle(fname)

    def load_all_runs(self, fname):
        self.df = pd.read_pickle(fname)
