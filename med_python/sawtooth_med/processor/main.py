import sys
import os
import argparse
import pkg_resources

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging
from sawtooth_sdk.processor.log import log_configuration
from sawtooth_sdk.processor.config import get_log_config
from sawtooth_sdk.processor.config import get_log_dir
from sawtooth_sdk.processor.config import get_config_dir

from sawtooth_med.processor.handler import MedicineHandler

from sawtooth_med.processor.config.med import MedConfig
from sawtooth_med.processor.config.med import \
    load_default_med_config
from sawtooth_med.processor.config.med import \
    load_toml_med_config
from sawtooth_med.processor.config.med import \
    merge_med_config

DISTRIBUTION_NAME = 'sawtooth_med'

def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-C', '--connect',help='Endpoint for the validator connection')

    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='Increase output sent to stderr')

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='print version information')

    return parser.parse_args(args)


def load_med_config(first_config):
    default_med_config = \
        load_default_med_config()
    conf_file = os.path.join(get_config_dir(), 'med.toml')

    toml_config = load_toml_med_config(conf_file)

    return merge_med_config(
        configs=[first_config, toml_config, default_med_config])


def create_med_config(args):
    return MedConfig(connect=args.connect)



def main(args = None):
    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)
    processor = None
    try:
        arg_config = create_med_config(opts)
        med_config = load_med_config(arg_config)
        processor = TransactionProcessor(url=med_config.connect)
        log_config = get_log_config(filename="med_log_config.toml")


        if log_config is None:
            log_config = get_log_config(filename="med_log_config.yaml")

        if log_config is not None:
            log_configuration(log_config=log_config)
        else:
            log_dir = get_log_dir()
            log_configuration(
                log_dir=log_dir,
                name="med-" + str(processor.zmq_id)[2:-1])

        init_console_logging(verbose_level=opts.verbose)

        handler = MedicineHandler()
        processor.add_handler(handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error: {}".format(e))
    finally:
        if processor is not None:
            processor.stop()
