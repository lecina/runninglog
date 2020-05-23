import os.path
import json

from runninglog.run import all_runs
from runninglog.utilities import utilities
from runninglog.constants import constants, blockNames
from runninglog.io import reader, writer
from runninglog.config import config


class RunningLog():
    def __init__(self, config=None):
        self.all_runs = all_runs.AllRuns()

        self.config = config

        self.added_runs = []

    def load_runs(self):
        """Load runs in input dir according to config
    
            Loads runs in input dir according to configuration
        """
        self.load_runs_in_dir(self.config.input_dir)

    def load_runs_in_dir(self, input_dir):
        """Load runs
    
            Loads runs in input dir

            Args:
                input_dir(str): Input directory
        """
        run_descs = reader.get_json_runs_in_subdirs(input_dir)

        self.added_runs = self.all_runs.load_runs(run_descs)

        print(f"Added {len(self.added_runs)} runs") 

    def compute_embedding(self):
        """Compute UMAP embedding
    
            Compute UMAP embedding
        """
        self.all_runs.compute_umap_projection()

    def group_added_runs_by_month(self):
        """Groups added runs by month in a dictionary
    
            Groups added runs by month in a dictionary.
        """
        grouped_runs = {}
        for run in self.added_runs:
            key = "/".join([str(run.date.year), str(run.date.month)])
            try:
                grouped_runs[key].append(run.orig_json_string)
            except KeyError:
                grouped_runs[key] = [run.orig_json_string]

        return grouped_runs

    def write_grouped_runs_to_file(self, grouped_runs):
        """Write grouped runs to file
    
            Write grouped runs to file
        """
        for (year_month, content_to_add) in grouped_runs.items():
            [year, month] = year_month.split("/")
            output_dir = os.path.join(self.config.raw_output_dir, year)
            output_filename = os.path.join(output_dir, month) + ".json"

            try:
                content = reader.read_json_file(output_filename)
            except FileNotFoundError:
                content = {constants.blockNames.FileParams.list: []}

            prev_runs = content[constants.blockNames.FileParams.list]
            to_add = [run for run in content_to_add if run not in prev_runs]
            content[constants.blockNames.FileParams.list].extend(to_add)

            output = json.dumps(content, indent=4, separators=(',', ': '))
            utilities.make_dir(output_dir)
            with open(output_filename, "w") as json_file:
                json_file.write(output)

    def save(self):
        """Save all runs
    
            Save all runs as defined in configuration file
        """
        # Save processed dataframes
        if blockNames.ConfigParams.csv in self.config.output_format:
            self.all_runs.save_as_csv(self.config)
        if blockNames.ConfigParams.pickle in self.config.output_format:
            self.all_runs.save_as_pickle(self.config)

        # Save all runs as pickle
        all_runs_fname = os.path.join(self.config.all_runs) + ".pkl"
        writer.to_pickle(self.all_runs, all_runs_fname)

        # Save raw data
        grouped_runs = self.group_added_runs_by_month()
        self.write_grouped_runs_to_file(grouped_runs)

    def load_previous_runs(self):
        """Load runs in raw directory
    
            Load runs in raw directory
        """
        self.load_runs_in_dir(self.config.raw_output_dir)
