from __future__ import print_function

import argparse
import getpass
import logging
import os
import traceback
import sys
import pkg_resources
import datetime

from sawtooth_PharmaChain.sawtooth_client import MedClient
from sawtooth_PharmaChain.med_exceptions import MedException


DISTRIBUTION_NAME = 'sawtooth_PharmaChain'

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
    formatter = ColoredFormatter(
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


def add_createMedicine_parser(subparsers , parent_parser):
    parser = subparse.add_parser(
        'createMedicine',
        help = 'Creates New Medicine Asset',
        description = 'Sends a transaction to create a medicine asset, it fails if name already taken.',
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
        'medicineKeyContent',
        type = str,
        help = 'Key Content present in medicine'
    )

    parser.add_argument(
        'medicineAllContents',
        type = str,
        help = 'All contents presoent in medicine'
    )

    parser.add_argument(
        'expirymonths',
        type = int,
        help = 'Months from current date in which medicine will expire'
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


def add_updateMedicine_parser(subparsers , parent_parser):
    parser = subparse.add_parser(
        'updateMedicine',
        help = 'Update Medicine information',
        parents = [parent_parser]
    )

    parser.add_argument(
        'medicineName',
        type = str,
        help = 'Unique Identifier for a Medicine'
    )

    parser.add_argument(
        'medicineID',
        type = str,
        help = 'Unique medicine Identifier'
    )

    parser.add_argument(
        'medicineKeyContent',
        type = str,
        help = 'Key Content present in medicine'
    )

    parser.add_argument(
        'medicineAllContents',
        type = str,
        help = 'All contents presoent in medicine'
    )

    parser.add_argument(
        'expirymonths',
        type = int,
        help = 'Months from current date in which medicine will expire'
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
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for asset to commit'
    )


def add_updateMedicineOwner_parser(subparsers , parent_parser):
    parser = subparse.add_parser(
        'updateMedicineOwner',
        help = 'Update Medicine current Owner',
        parents = [parent_parser]
    )

    parser.add_argument(
        'medicineName',
        type = str,
        help = 'Unique Identifier for a Medicine'
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
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for asset to commit'
    )


def add_deleteMedicine_parser(subparsers , parent_parser):
    parser = subparse.add_parser(
        'deleteMedicine',
        help = 'Delete a medicine asset',
        parents = [parent_parser]
    )

    parser.add_argument(
        'medicineName',
        type = str,
        help = 'Unique Identifier for a Medicine'
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
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for asset to commit'
    )


def add_show_parser(subparsers , parent_parser):
    parser = subparse.add_parser(
        'show',
        help = 'Show a medicine asset',
        parents = [parent_parser]
    )

    parser.add_argument(
        'medicineName',
        type = str,
        help = 'Unique Identifier for a new Medicine'
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


def add_list_parser(subparsers , parent_parser):
    parser = subparse.add_parser(
        'list',
        help = 'List all the medicine assets',
        parents = [parent_parser]
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


def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output')

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='display version information')

    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to perform action related to medicine asset.',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_createMedicine_parser(subparsers, parent_parser)
    add_list_parser(subparsers, parent_parser)
    add_show_parser(subparsers, parent_parser)
    add_updateMedicine_parser(subparsers, parent_parser)
    add_updateMedicineOwner_parser(subparsers , parent_parser)
    add_deleteMedicine_parser(subparsers, parent_parser)

    return parser


def do_createMedicine(args):
    medicineName = args.medicineName
    medicineID = args.medicineID
    medicineKeyContent = args.medicineKeyContent
    medicineAllContents = args.medicineAllContents
    manufactureDate = datetime.date.today()
    expiryDate = manufactureDate + datetime.timedelta((args.expirymonths)*365/12)

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = MedClient(base_url = url , keyfile = keyfile)

    if args.wait and args.wait > 0:
        response = client.createMedicine(
            medicineName,
            medicineID,
            medicineKeyContent,
            medicineAllContents,
            manufactureDate,
            expiryDate,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password
        )
    else:
        response = client.createMedicine(
            medicineName,
            medicineID,
            medicineKeyContent,
            medicineAllContents,
            manufactureDate,
            expiryDate,
            auth_user = auth_user,
            auth_password = auth_password
        )
    print("Response : {}".format(response))


def do_updateMedicine(args):
    medicineName = args.medicineName
    medicineID = args.medicineID
    medicineKeyContent = args.medicineKeyContent
    medicineAllContents = args.medicineAllContents
    manufactureDate = datetime.date.today()
    expiryDate = manufactureDate + datetime.timedelta((args.expirymonths)*365/12)

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = MedClient(base_url = url , keyfile = keyfile)

    if args.wait and args.wait > 0:
        response = client.updateMedicine(
            medicineName,
            medicineID,
            medicineKeyContent,
            medicineAllContents,
            manufactureDate,
            expiryDate,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password
        )
    else:
        response = client.updateMedicine(
            medicineName,
            medicineID,
            medicineKeyContent,
            medicineAllContents,
            manufactureDate,
            expiryDate,
            auth_user = auth_user,
            auth_password = auth_password
        )
    print("Response : {}".format(response))


def do_updateMedicineOwner(args):
    medicineName = args.medicineName

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = MedClient(base_url = url , keyfile = keyfile)

    if args.wait and args.wait > 0:
        response = client.updateMedicineOwner(
            medicineName,
            medicineID = '',
            medicineKeyContent = '',
            medicineAllContents = '',
            manufactureDate = '',
            expiryDate = '',
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password
        )
    else:
        response = client.updateMedicineOwner(
            medicineName,
            medicineID = '',
            medicineKeyContent = '',
            medicineAllContents = '',
            manufactureDate= '',
            expiryDate= '',
            auth_user = auth_user,
            auth_password = auth_password
        )
    print("Response : {}".format(response))


def do_deleteMedicine(args):
    medicineName = args.medicineName

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = MedClient(base_url = url , keyfile = keyfile)

    if args.wait and args.wait > 0:
        response = client.deleteMedicine(
            medicineName,
            medicineID = '',
            medicineKeyContent = '',
            medicineAllContents = '',
            manufactureDate = '',
            expiryDate = '',
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password
        )
    else:
        response = client.deleteMedicine(
            medicineName,
            medicineID = '',
            medicineKeyContent = '',
            medicineAllContents = '',
            manufactureDate= '',
            expiryDate= '',
            auth_user = auth_user,
            auth_password = auth_password
        )
    print("Response : {}".format(response))


def do_show(args):
    medicineName = args.medicineName

    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)

    client = MedClient(base_url=url, keyfile=None)

    data = client.show(medicineName, auth_user=auth_user, auth_password=auth_password)

    if data is not None:
        print("DATA fetched, code to retrieve")
    else:
        raise MedException("Medicine not found: {}".format{medicineName})

def do_list(args):
    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)

    client = MedClient(base_url=url, keyfile=None)

    medicine_list = [
        game.split(',')
        for medicines in client.list(auth_user=auth_user,
                                 auth_password=auth_password)
        for medicine in medicines.decode().split('|')
    ]

    if medicine_list is not None:
        print(medicine_list[0]+ "\n Write More code to retrieve!")
    else:
        raise MedException("Could not retireve List")


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

    if args.command == 'createMedicine':
        do_createMedicine(args)

    elif args.command == 'updateMedicine':
        do_updateMedicine(args)

    elif args.command == 'updateMedicineOwner':
        do_updateMedicineOwner(args)

    elif args.command == 'deleteMedicine':
        do_deleteMedicine(args)

    elif args.command == 'list':
        do_list(args)

    elif args.command == 'show':
        do_show(args)

    else:
        raise MedException("Invalid Command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except MedException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
