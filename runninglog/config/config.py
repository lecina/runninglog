import os

from runninglog.io import reader
from runninglog.constants import blockNames


class Config():
    def __init__(self):
        self.output_dir = "data"
        self._raw_output_dir = "raw"
        self._processed_output_dir = "processed"

        self.input_dir = "input_dir"

        self._all_runs = "all_runs"
        self._df_name = "df"
        self._df_struct_name = "df_struct"

        self.output_format = ['csv', 'pickle']

    def __str__(self):
        return "\n".join(
            [
                self.output_dir,
                self.raw_output_dir,
                self.processed_output_dir,
                self.input_dir,
                self.all_runs,
                self.df_name,
                self.df_struct_name,
                "\n".join(self.output_format)
            ]
        )

    @property
    def raw_output_dir(self):
        """Get raw_output_dir full filename"""
        return os.path.join(self.output_dir, self._raw_output_dir)

    @property
    def processed_output_dir(self):
        """Get processed_output_dir full filename"""
        return os.path.join(self.output_dir, self._processed_output_dir)

    @property
    def all_runs(self):
        """Get all_runs full filename"""
        return os.path.join(self.processed_output_dir, self._all_runs)

    @property
    def df_name(self):
        """Get df full filename"""
        return os.path.join(self.processed_output_dir, self._df_name)

    @property
    def df_struct_name(self):
        """Get df struct full filename"""
        return os.path.join(self.processed_output_dir, self._df_struct_name)

    def load_config_file(self, config_filename = ""):
        """Reads configuration file

            Reads configuration file in JSON format. If not provided, using
            default location

            Args:
                config_filename(str): Filename path
        """
        if config_filename != "":
            config = reader.read_json_file(config_filename)
            self.load_config(config)

    def load_config(self, config):
        """Loads configuration in dict

            Loads configuration in dict

            Args:
                config_desc(dict): Desc dict
        """

        try:
            od = config[blockNames.ConfigParams.output_dir]
            self.output_dir = od
        except KeyError:
            pass

        try:
            rod = config[blockNames.ConfigParams.raw_output_dir]
            self._raw_output_dir = os.path.join(self.output_dir, rod)
        except KeyError:
            pass

        try:
            pod = config[blockNames.ConfigParams.processed_output_dir]
            self._processed_output_dir = os.path.join(self.output_dir, pod)
        except KeyError:
            pass

        try:
            id_ = config[blockNames.ConfigParams.input_dir]
            self.input_dir = id_
        except KeyError:
            pass

        try:
            df_name = config[blockNames.ConfigParams.df_name]
            self._df_name = df_name
        except KeyError:
            pass

        try:
            df_struct_name = config[blockNames.ConfigParams.df_struct_name]
            self._df_struct_name = df_struct_name
        except KeyError:
            pass

        try:
            output_fmts = config[blockNames.ConfigParams.output_fmt]
        except KeyError:
            output_fmts = self.output_format

        if isinstance(output_fmts, str):
            self.output_format = [output_fmts]
        else:
            self.output_format = output_fmts
