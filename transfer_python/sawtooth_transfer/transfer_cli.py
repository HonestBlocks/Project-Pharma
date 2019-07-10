from __future__ import print_function

import argparse
import getpass
import logging
import os
import traceback
import sys
import pkg_resources
import datetime
import colorlog

from sawtooth_transfer.transfer_client import TransferClient
from sawtooth_transfer.transfer_exceptions import TransferException

DISTRIBUTION_NAME = 'sawtooth_transfer'

DEFAULT_URL = 'http://127.0.0.1:8008'

def _get_url(args):
    return DEFAULT_URL if args.url is None else args.url


def _get_keyfile(args):
    username = getpass.getuser() if args.username is None else args.username
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, username)


def _get_auth_info(args):
    auth_user = args.auth_user
    auth_password = args.auth_password
    if auth_user is not None and auth_password is None:
        auth_password = getpass.getpass(prompt="Auth Password: ")

    return auth_user, auth_password


def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)

    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)

    return clog


def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))

def add_createBox_parser(subparsers , parent_parser):
    parser = subparsers.add_parser(
        'createBox',
        help = 'Creates a box asset to store medicines',
        description = 'Sends a transaction to create a box asset, it fails if medicine units are less or asset not present.',
        parents = [parent_parser]
    )

    parser.add_argument(
        'medicineName',
        type = str,
        help = 'Unique Identifier for a new Medicine'
    )

    parser.add_argument(
        'medicineID',
        type = str,
        help = 'Unique medicine Identifier'
    )

    parser.add_argument(
        'units',
        type = int,
        help = 'No. of units to be packed'
    )

    parser.add_argument(
        '--url',
        type = str,
        help = 'Specify URL of RestAPI'
    )

    parser.add_argument(
        '--username',
        type = str,
        help = 'Identify name of Owner\'s private key file'
    )

    parser.add_argument(
        '--key-dir',
        type = str,
        help = 'Identify directory of Owner\'s private ke file'
    )

    parser.add_argument(
        '--auth-user',
        type = str,
        help = 'Specify username for authentication of RestAPI'
    )

    parser.add_argument(
        '--auth-password',
        type = str,
        help = 'Specify password for authentication of RestAPI'
    )

    parser.add_argument(
        '--disable-client-validation',
        action='store_true',
        default=False,
        help='disable client validation'
    )

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for asset to commit'
    )

def add_updateBox_parser(subparsers, parent_parser):
    



def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to perform action',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_createBox_parser(subparsers, parent_parser)
    add_updateBox_parser(subparsers, parent_parser)
    add_createshipment_parser(subparsers, parent_parser)
    add_updateShipment_parser(subparsers, parent_parser)
    add_deleteShipment_parser(subparsers, parent_parser)

    return parser



def main(prog_name = os.path.basename(sys.argv[0]), args = None):
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)

    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose

    setup_loggers(verbose_level=verbose_level)

    if args.command == 'createBox':
        do_createBox(args)

    elif args.command == 'updateBox':
        do_updateBox(args)

    elif args.command == 'createShipment':
        do_createShipment(args)
        
    elif args.command == 'updateShipment':
        do_updateShipment(args)

    elif args.command == 'deleteShipment':
        do_deleteShipment(args)

    elif args.command == 'list':
        do_list(args)

    elif args.command == 'show':
        do_show(args)

    else:
        raise TransferException("Invalid Command: {}".format(args.command))



def main_wrapper():
    try:
        main()
    except TransferException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
