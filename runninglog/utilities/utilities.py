import os.path
import shutil
import pandas as pd


def cleanup(f):
    """
        Remove dir if exists

        :param f: Dir to remove
        :type f: str
    """
    if os.path.exists(f):
        shutil.rmtree(f)


def rm_file(f):
    """
        Remove file if exists

        :param f: File to remove
        :type f: str
    """
    if os.path.isfile(f):
        os.remove(f)


def make_dir(outputDir):
    """
        Makes dir

        :param outputDir: Dir filename
        :type outputDir: str
    """
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    if (a is None and b is not None) or (a is not None and b is None):
        return False
    elif a is None and b is None:
        return True

    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
