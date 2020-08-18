import pickle
import os.path

import pandas as pd
import numpy as np
import umap
from sklearn.preprocessing import MinMaxScaler

from runninglog.io import reader, writer
from runninglog.run import single, types, aggregator
from runninglog.constants import blockNames
from runninglog.utilities import utilities


class AllRuns():
    def __init__(self):
        self.runs = []
        self.structures = []

        self.df = pd.DataFrame()
        self.df_structures = pd.DataFrame()

        self.df_agg_w = pd.DataFrame()
        self.df_agg_m = pd.DataFrame()
        self.df_agg_y = pd.DataFrame()

    def load_runs(self, runs, verbose=True):
        """Loads all runs

            Loads all runs in list

            Args:
                runs(list): List of runs to load
                verbose(bool): Show more output

            Returns:
                list: List of added files
        """
        if not isinstance(runs, list):
            error = "runs must be a list"
            raise Exception(error)

        all_runs = self.build_runs(runs)

        parsed_single_runs = self.add_runs(all_runs)

        return parsed_single_runs

    def build_run(self, run_desc):
        """Builds the run(s) in dictionary

            Builds the run (or runs if there is more than one) in the
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

        if not isinstance(run_desc, dict):
            error = f"Input must be a dict"
            logging.exception(error)
            raise Exception(error)

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

    def build_runs(self, runs_to_build):
        """Builds the runs in list of dictionaries

            Builds the runs in the input list of dictionaries

            Args:
                run_desc(list): Runs to build

            Returns:
                list: list of single runs
        """

        if not isinstance(runs_to_build, list):
            error = "Input must be a dict"
            logging.exception(error)
            raise Exception(error)

        all_runs = []
        for run in runs_to_build:
            built_runs = self.build_run(run)
            all_runs.extend(built_runs)
        return all_runs

    def add_run(self, run):
        """Adds the run if it is not found

            Adds the SingleRun if it is not found, so that runs are not
            duplicated.

            Args:
                run(SinlgeRun): Single run to be added

            Returns:
                bool: True if run was added
        """

        if not isinstance(run, single.SingleRun):
            error = "Input must be a SingleRun"
            logging.exception(error)
            raise Exception(error)

        if run in self.runs:
            return False

        self.runs.append(run)
        self.structures.extend(run.structure)

        self.df = self.df.append(run.as_dict(), ignore_index=True)
        self.df = self.df.astype({blockNames.Colnames.feeling: 'float32'})

        self.df_structures = pd.concat(
                            [self.df_structures, run.get_structure_as_df()],
                            axis=0, ignore_index=True
        )

        return True

    def add_runs(self, runs):
        """Adds the runs if not found in self.runs

            Adds the runs if not found in self.runs, so that runs are not
            duplicated. Equivalent to add_run for list of runs

            Args:
                runs(list): List of single runs to be potentially added

            Returns:
                list: added runs
        """

        if not isinstance(runs, list):
            error = "Input must be a list"
            logging.exception(error)
            raise Exception(error)

        parsed_single_runs = []
        for run in runs:
            added_run = self.add_run(run)

            if added_run:
                parsed_single_runs.append(run)

        return parsed_single_runs

    def compute_umap_projection(
                self, cols=['climb', 'distance', 'time', 'avg_pace']):
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

        self.df['umap_X1'] = embedding[:, 0]
        self.df['umap_X2'] = embedding[:, 1]

    def compute_df_aggregations(self):
        """Aggregate df

            Aggregate df weekly, monthly, and yearly
        """
        self.df_agg_w = self.agg_df('week')
        self.df_agg_m = self.agg_df('month')
        self.df_agg_y = self.agg_df('year')

    def agg_df(self, time_option):
        return aggregator.agg_df(self.df, time_option)

    def save_as_csv(self, config):
        """Saves all runs as csv

            Saves all runs as csv

            Args:
                config(Config): Config object with filenames
        """

        fname = config.df_name + ".csv"
        writer.dataframe_to_csv(self.df, fname)

        fname = config.df_struct_name + ".csv"
        writer.dataframe_to_csv(self.df_structures, fname)

        fname = config.df_agg_name + "_w.csv"
        writer.dataframe_to_csv(self.df_agg_w, fname)

        fname = config.df_agg_name + "_m.csv"
        writer.dataframe_to_csv(self.df_agg_m, fname)

        fname = config.df_agg_name + "_y.csv"
        writer.dataframe_to_csv(self.df_agg_y, fname)

    def save_as_pickle(self, config):
        """Saves all runs as pkl

            Saves all runs as pkl

            Args:
                config(Config): Config object with filenames
        """

        fname = config.df_name + ".pkl"
        writer.dataframe_to_pickle(self.df, fname)

        fname = config.df_struct_name + ".pkl"
        writer.dataframe_to_pickle(self.df_structures, fname)

        fname = config.df_agg_name + "_w.pkl"
        writer.dataframe_to_pickle(self.df_agg_w, fname)

        fname = config.df_agg_name + "_m.pkl"
        writer.dataframe_to_pickle(self.df_agg_m, fname)

        fname = config.df_agg_name + "_y.pkl"
        writer.dataframe_to_pickle(self.df_agg_y, fname)
