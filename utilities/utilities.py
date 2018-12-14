import os.path
import shutil

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


