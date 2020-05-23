import pickle
import os.path
import pandas as pd

from runninglog.utilities import utilities

def dataframe_to_pickle(df, fname):
    """Write dataframe to pickle file

        Write dataframe to pickle file. Creates folder if
        does not exist

        Args:
            df(DataFrame): DataFrame to write
            fname(str): Pickle filename
    """
    utilities.make_dir(os.path.split(fname)[0])
    utilities.rm_file(fname)

    df.to_pickle(fname)

def dataframe_to_csv(df, fname, encoding='utf-8', round_float_cols=True):
    """Write dataframe to csv file

        Write dataframe to csv file. Removes file if exists.

        Args:
            df(DataFrame): DataFrame to write
            fname(str): CSV filename
            encoding(str): Encoding
            round_float_cols(bool): Round columns with floats
    """
    if round_float_cols:
        cols = df.select_dtypes("floating").columns
        decimals = pd.Series([2] * len(cols), index=cols)
        df = df.round(decimals)

    utilities.make_dir(os.path.split(fname)[0])
    utilities.rm_file(fname)
    df.to_csv(fname, encoding=encoding)

def to_pickle(obj, fname):
    """Write object to pickle

        Write object to pickle. Removes file if exists

        Args:
            obj(Object): Object to write

        Note:
            Watch out for pickle objects, as they can be hacked.
            Example: https://realpython.com/python-pickle-module/
    """
    utilities.make_dir(os.path.split(fname)[0])
    utilities.rm_file(fname)
    pickle.dump(obj, open(fname, "wb"))
