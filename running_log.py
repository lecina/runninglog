from all_runs import all_runs
from utilities import utilities
from constants import constants

class RunningLog():
    def __init__(self, *args, **kwargs):
        
        self.allRuns = all_runs.AllRuns()
        if len(args) == 1:
            directory = args[0]
            self.allRuns.load_files_in_dir(directory)

    def generate_empty_json(self):
        fname_template = os.path.join(constants.TO_LOAD_FOLDER,
                                    constants.JSON_TEMPLATE_OUTPUT_NAME)
        fname = fname_template%"" 
        i=1
        while os.path.isfile(fname):
            suffix = "_%d"%i
            fname = fname_template%suffix
            i += 1
            
        utilities.make_dir(constants.TO_LOAD_FOLDER)
        with open(fname, "w") as json_file:
            json_file.write(constants.EMPTY_JSON)

        print "Generated: %s"%fname

    def load_files_to_load(self):
        directory = constants.TO_LOAD_FOLDER
        self.allRuns.load_files_in_dir(directory)


def main():
    allRuns = all_runs.AllRuns()

if __name__ == "__main__":
    main()
