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

from sawtooth_transfer.processor.handler import TransferHandler

from sawtooth_transfer.processor.config.transfer import TransferConfig
from sawtooth_transfer.processor.config.transfer import \
    load_default_transfer_config
from sawtooth_transfer.processor.config.transfer import \
    load_toml_transfer_config
from sawtooth_transfer.processor.config.transfer import \
    merge_transfer_config

DISTRIBUTION_NAME = 'sawtooth_transfer'

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


def load_transfer_config(first_config):
    default_transfer_config = \
        load_default_transfer_config()
    conf_file = os.path.join(get_config_dir(), 'transfer.toml')

    toml_config = load_toml_transfer_config(conf_file)

    return merge_transfer_config(
        configs=[first_config, toml_config, default_transfer_config])


def create_transfer_config(args):
    return TransferConfig(connect=args.connect)


def main(args = None):
    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)
    processor = None
    try:
        arg_config = create_transfer_config(opts)
        transfer_config = load_transfer_config(arg_config)
        processor = TransactionProcessor(url=transfer_config.connect)
        log_config = get_log_config(filename="transfer_log_config.toml")


        if log_config is None:
            log_config = get_log_config(filename="transfer_log_config.yaml")

        if log_config is not None:
            log_configuration(log_config=log_config)
        else:
            log_dir = get_log_dir()
            log_configuration(
                log_dir=log_dir,
                name="transfer" + str(processor.zmq_id)[2:-1])

        init_console_logging(verbose_level=opts.verbose)

        handler = TransferHandler()
        processor.add_handler(handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error: {}".format(e))
    finally:
        if processor is not None:
            processor.stop()
