import argparse

from runninglog.runninglog import runninglog
from runninglog.config import config
from runninglog.utilities import utilities

def parseArgs():
    desc_str = "Running log program.\n"\
                "Processes JSON files with running events and generates\n"\
                "output for further exploitation"
    parser = argparse.ArgumentParser(description=desc_str)

    parser.add_argument("-t", "--template", action='store_true', help="Generate template file")
    parser.add_argument("-f", "--force", action='store_true', help="Force reading previous runs")
    parser.add_argument("-c", "--config_file", type=str, default="", help="Config file path")

    args = parser.parse_args()
    return args

def generate_empty_json(self, config):
    fname_template = os.path.join(config.input_dir,
                                constants.JSON_TEMPLATE_OUTPUT_NAME)
    fname = fname_template%"" 
    i=1
    while os.path.isfile(fname):
        suffix = "_%d"%i
        fname = fname_template%suffix
        i += 1
        
    utilities.make_dir(config.input_dir)
    with open(fname, "w") as json_file:
        json_file.write(constants.EMPTY_JSON)

    print ("Generated: %s"%fname)

def main():
    args = parseArgs()

    if args.template:
        print ("Generating template\n")
        generate_empty_json()
        return

    configuration = config.Config()
    configuration.load_config_file(args.config_file)

    rl = runninglog.RunningLog(configuration)

    if args.force:
        rl.load_previous_runs()
    else:
        utilities.cleanup(configuration.output_dir)

    print (f"Reading runs from {configuration.input_dir}")
    rl.load_runs()
    print ("Computing embedding")
    rl.compute_embedding()
    print ("Finished!")

    rl.save()

if __name__ == "__main__":
    main()
