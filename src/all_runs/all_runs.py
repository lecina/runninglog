from reader import reader
from single_run import single_run
from constants import constants, blockNames
from utilities import utilities

import os
import fnmatch
import pandas as pd
import numpy as np
import pickle
import umap
from sklearn.preprocessing import MinMaxScaler

class AllRuns():
    def __init__(self):
        self.df = pd.DataFrame()
        self.structures = pd.DataFrame() #TODO: append structures

    def read_single_run(self, filename, verbose=True):
        if verbose: print "Reading", filename
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

    def append_single_run_if_not_present(self, sr):
        sr_ds = pd.Series(sr.as_dict())
    
        if self.df.size == 0:
            already_added = False
        else:
            already_added = sum((self.df.values==sr_ds.values).all(axis=1))

        if not already_added:
            self.df = self.df.append(sr_ds, ignore_index=True)
            self.structures = pd.concat([self.structures, sr.get_structure_as_df()], axis=0)

        added_sr = not already_added
        return added_sr

    def get_json_files_in_subdirs(self, directory):
        file_list = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, '*.json'):
                file_list.append(os.path.join(root, filename))
        return file_list

    def load_files_in_dir(self, directory, verbose=True):
        file_list = self.get_json_files_in_subdirs(directory)

        if len(file_list) == 0:
            if verbose: 
                print "No files to read!"
            return []

        parsed_single_runs = []
        for f in file_list:
            jsonFile = open(f, 'r').read()
            if jsonFile == constants.EMPTY_JSON or jsonFile == "":
                if verbose: 
                    print "Empty json file: \"%s\"!\nCleaning it up!!"%f
                utilities.rm_file(f)
            else:
                #TODO: add json validator
                srs = self.read_single_run(f, verbose) 
                if type(srs) is not list:
                    srs = [srs]
                
                for sr in srs:
                    added_sr = self.append_single_run_if_not_present(sr)

                    if added_sr:
                        parsed_single_runs.append(sr)
                    elif verbose==True:
                        print "Not adding already added move:", sr.as_dict()
                        print "in %s"%f

        return parsed_single_runs

    def compute_umap_projection(self, cols=['climb', 'distance', 'time', 'avg_pace']):
        """
            Dimensionality reduction.
            Adds two columns: umap_X1, uma_X2 with projection
        """
        reducer = umap.UMAP(n_neighbors=15, min_dist=0.1)

        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(self.df[cols])
        embedding = reducer.fit_transform(df_scaled)
        df_embedding = pd.DataFrame(embedding, columns=['umap_X1', 'umap_X2'])

        self.df = pd.concat([self.df, df_embedding], axis=1, sort=False)

    def save_all_runs(self, fname):
        self.df.to_pickle(fname)

    def load_all_runs(self, fname):
        self.df = pd.read_pickle(fname)

    def save_all_runs_as_csv(self, fname):
        self.df.to_csv(fname, encoding='utf-8')

    def load_all_runs_from_csv(self, fname):
        self.df = pd.from_csv(fname)

    def save_all_runs_structures(self, fname):
        self.structures.to_pickle(fname)

    def load_all_runs_structures(self, fname):
        self.structures = pd.read_pickle(fname)

    def save_all_runs_structures_as_csv(self, fname):
        self.structures.to_csv(fname, encoding='utf-8')

    def load_all_runs_structures_from_csv(self, fname):
        self.structures = pd.from_csv(fname)
