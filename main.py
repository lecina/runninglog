import argparse
import logging
import logging.config

from runninglog.runninglog import runninglog
from runninglog.config import config
from runninglog.utilities import utilities


def parseArgs():
    desc_str = "Running log program.\n"\
                "Processes JSON files with running events and generates\n"\
                "output for further exploitation"
    parser = argparse.ArgumentParser(description=desc_str)

    parser.add_argument("-t", "--template", action='store_true',
                        help="Generate template file")
    parser.add_argument("-f", "--force", action='store_true',
                        help="Force reading previous runs")
    parser.add_argument("-c", "--config_file", type=str, default="",
                        help="Config file path")

    args = parser.parse_args()
    return args

def logging_params():
    return dict(
            version = 1,
            formatters = {
                'f': {'format':
                    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
                },
            handlers = {
                'h': {'class': 'logging.StreamHandler',
                    'formatter': 'f',
                    'level': logging.DEBUG}
                },
            root = {
                'handlers': ['h'],
                'level': logging.DEBUG,
                },
    )

def generate_empty_json(config):
    fname_template = os.path.join(config.input_dir,
                                  constants.JSON_TEMPLATE_OUTPUT_NAME)
    fname = fname_template % ""
    i = 1
    while os.path.isfile(fname):
        suffix = "_%d" % i
        fname = fname_template % suffix
        i += 1

    utilities.make_dir(config.input_dir)
    with open(fname, "w") as json_file:
        json_file.write(constants.EMPTY_JSON)

    logging.info(f"Generated: {fname}")

def main():
    logging.config.dictConfig(logging_params())
    logger = logging.getLogger()

    args = parseArgs()

    if args.template:
        logger.info("Generating template\n")
        generate_empty_json()
        return

    configuration = config.Config()
    configuration.load_config_file(args.config_file)

    rl = runninglog.RunningLog(configuration)

    if args.force:
        logger.info(f"Loading runs in {configuration.raw_output_dir}")
        rl.load_previous_runs()
    else:
        logger.info(f"Cleaning up {configuration.output_dir}")
        utilities.cleanup(configuration.output_dir)

    logger.info(f"Reading runs from {configuration.input_dir}")
    rl.load_runs()
    logger.info("Computing aggregations")
    rl.compute_aggregations()
    logger.info("Computing UMAP embedding")
    rl.compute_embedding()
    logger.info("Finished!")

    rl.save()


if __name__ == "__main__":
    main()
