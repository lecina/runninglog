import pickle

import pandas as pd
import numpy as np
import umap
from sklearn.preprocessing import MinMaxScaler

from runninglog.io import reader
from runninglog.run import single, types
from runninglog.constants import constants, blockNames
from runninglog.utilities import utilities

class AllRuns():
    def __init__(self):
        self.runs = []
        self.structures = []

        self.df = pd.DataFrame()
        self.df_structures = pd.DataFrame()

    def read_run_in_file(self, filename, verbose=True):
        """Reads the run(s) in filename

            Loads the run (or runs if there is more than one) in the
            filename

            Args:
                filename(str): Path to the filename to be read
                verbose(bool): True for enhanced output

            Returns:
                list: list of single runs

            Note:
                It accepts a filename in json format with either one or
                a list of single runs. In the latter, the list is
                defined with the key in `blockNames.FileParams.list`
        """

        if verbose:
            print ("Reading", filename)

        parsed_json = reader.read_file(filename)

        if parsed_json == constants.EMPTY_JSON or parsed_json == "":
            if verbose:
                print (f"Empty file: \"{f}\"!")

        return self.read_run(parsed_json)

    def read_run(self, run_desc):
        """Reads the run(s) in dictionary

            Reads the run (or runs if there is more than one) in the
            input dictionary

            Args:
                run_desc(dict): Dictionary used as single run input

            Returns:
                list: list of single runs

            Note:
                It accepts a run_desc in dict format with either one or
                a list of single runs. In the latter, the list is
                defined with the key in `blockNames.FileParams.list`
        """

        try:
            run_dicts = run_desc[blockNames.FileParams.list]
        except KeyError:
            run_dicts = [run_desc]

        single_runs = []
        for run_dict in run_dicts:
            single_run = single.SingleRun()
            single_run.load(run_dict)
            single_runs.append(single_run)

        return single_runs

    def add_run(self, run):
        """Adds the run if it is not found

            Adds the run if it is not found, so that runs are not duplicated

            Args:
                run(SinlgeRun): Single run to be added

            Returns:
                bool: True if run was added
        """
        if run in self.runs:
            return False
    
        self.runs.append(run)
        self.structures.extend(run.structure)

        self.df = self.df.append(run.as_dict(), ignore_index=True)
        self.df_structures = pd.concat([
                                        self.df_structures, 
                                        run.get_structure_as_df(),
                                        ],
                                        axis=0, ignore_index=True)

        return True

    def load_files_in_dir(self, directory, verbose=True):
        """Loads all runs from all JSON files in dir

            Loads all runs from all JSON files in dir

            Args:
                directory(str): Root directory
                verbose(bool): Show more output

            Returns:
                list: List of added files
        """
        file_list = reader.get_json_files_in_subdirs(directory)

        parsed_single_runs = []
        for f in file_list:
            runs = self.read_run_in_file(f, verbose) 

            for run in runs:
                added_run = self.add_run(run)

                if added_run:
                    parsed_single_runs.append(run)
                    # TODO: add event to log

        return parsed_single_runs

    def compute_umap_projection(self, cols=['climb', 'distance', 'time', 'avg_pace']):
        """Compute UMAP projection

            Compute umap projection.
            Adds two columns to self.df: umap_X1, umap_X2 with the projection

            Args:
                cols(list): list of input columns to UMAP
        """
        reducer = umap.UMAP(n_neighbors=15, min_dist=0.1)

        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(self.df[cols])
        embedding = reducer.fit_transform(df_scaled)

        self.df['umap_X1'] = embedding[:,0]
        self.df['umap_X2'] = embedding[:,1]

    def save_all_runs(self, fname):
        """Saves runs as pickle object

            Saves runs as pickle object

            Args:
                fname(str): Filename to save
        """
        self.df.to_pickle(fname)

    def load_all_runs(self, fname):
        """Loads runs from pickle object

            Loads runs from pickle object

            Args:
                fname(str): Filename to load
        """
        self.df = pd.read_pickle(fname)

    def save_all_runs_as_csv(self, fname):
        """Saves runs as csv

            Saves runs as csv

            Args:
                fname(str): Filename to save
        """
        columns = ['avg_pace', 'vspeed']

        basic_types = types.BASIC_RUN_TYPES_DICTIONARY.values()
        dist_cols = ["dist{}".format(t) for t in basic_types]
        time_cols = ["time{}".format(t) for t in basic_types]
        pace_cols = ["pace{}".format(t) for t in basic_types]

        columns.extend(dist_cols)
        columns.extend(time_cols)
        columns.extend(pace_cols)

        decimals = pd.Series([2] * len(columns), index=columns)
        df_to_save = self.df.round(decimals)

        df_to_save.to_csv(fname, encoding='utf-8')

    def load_all_runs_from_csv(self, fname):
        """Loads runs from csv

            Loads runs from csv

            Args:
                fname(str): CSV filename
        """
        self.df = pd.from_csv(fname)

    def save_all_runs_structures(self, fname):
        """Save runs structure as picke

            Save runs structure as pickle

            Args:
                fname(str): Pickle filename
        """
        self.df_structures.to_pickle(fname)

    def load_all_runs_structures(self, fname):
        """Load runs structure from pickle

            Load runs structure from pickle

            Args:
                fname(str): Pickle filename
        """
        self.df_structures = pd.read_pickle(fname)

    def save_all_runs_structures_as_csv(self, fname):
        """Save runs structure as csv

            Save runs structure as csv

            Args:
                fname(str): CSV filename
        """
        columns = ['avg_pace', 'vspeed']
        decimals = pd.Series([2] * len(columns), index=columns)
        df_to_save = self.df_structures.round(decimals)
        self.df_to_save.to_csv(fname, encoding='utf-8')

    def load_all_runs_structures_from_csv(self, fname):
        """Load runs structure from csv

            Load runs structure from csv

            Args:
                fname(str): CSV filename
        """
        self.df_structures = pd.from_csv(fname)
