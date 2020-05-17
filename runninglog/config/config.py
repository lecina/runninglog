import os

from runninglog.io import reader
from runninglog.constants import blockNames


class Config():
    def __init__(self):
        self.output_dir = "data"
        self.raw_output_dir = os.path.join(self.output_dir, "raw")
        self.processed_output_dir = of.path.join(self.output_dir, "processed")

        self.input_dir = "to_load"

    def read_config(self, config_filename = ""):
        """Reads configuration file

            Reads configuration file in JSON format. If not provided, using
            default location

            Args:
                config_filename(str): Filename path

            Notes:
                Default location is runninglog/config/config.json
        """
        if config_filename == "":
            current_dir = os.path.split(__file__)[0]
            config_filename = os.path.join(current_dir, 'config.json')

        config = reader.read_json_file(config_filename)

        try:
            od = config[blockNames.ConfigParams.output_dir]
            self.output_dir = od
        except KeyError:
            pass

        try:
            rod = config[blockNames.ConfigParams.raw_output_dir]
            self.raw_output_dir = os.path.join(self.output_dir, rod)
        except KeyError:
            pass

        try:
            pod = config[blockNames.ConfigParams.processed_output_dir]
            self.processed_output_dir = os.path.join(self.output_dir, pod)
        except KeyError:
            pass

        try:
            id_ = config[blockNames.ConfigParams.input_dir]
            self.input_dir = id_
        except KeyError:
            pass
