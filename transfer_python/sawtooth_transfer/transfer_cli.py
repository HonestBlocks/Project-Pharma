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
    parser = subparsers.add_parser(
        'updateBox',
        help = 'Creates a box asset to store medicines',
        description = 'Sends a transaction to update a box asset, it fails if medicine units are less or asset not present.',
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
        'boxID',
        type = int,
        help = 'ID of Box'
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


def add_createshipment_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'createShipment',
        help = 'Create a shipment with n boxes',
        parents = [parent_parser]
    )

    parser.add_argument(
        'boxIDArray',
        type = str,
        help = 'All boxes ID to be included in shipment'
    )

    parser.add_argument(
        'origin',
        type = str,
        help = 'Origin address'
    )

    parser.add_argument(
        'destination',
        type = str,
        help = 'Destination Address'
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


def add_updateShipmentStatus_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'updateShipmentStatus',
        help = 'Update a shipment with n boxes',
        parents = [parent_parser]
    )

    parser.add_argument(
        'shipmentID',
        type = str,
        help = 'Shipment ID'
    )

    parser.add_argument(
        'shipmentStatus',
        type = str,
        help = 'current address of shipment'
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


def add_deleteShipment_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'deleteShipment',
        help = 'Delete a shipment with n boxes',
        parents = [parent_parser]
    )

    parser.add_argument(
        'shipmentID',
        type = str,
        help = 'Shipment ID'
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
    parser = subparsers.add_parser(
        'show',
        help = 'Show an asset',
        parents = [parent_parser]
    )

    parser.add_argument(
        'ID',
        type = str,
        help = 'Unique Identifier'
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
    parser = subparsers.add_parser(
        'list',
        help = 'List all the assets',
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
        description='Provides subcommands to perform action',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_createBox_parser(subparsers, parent_parser)
    add_updateBox_parser(subparsers, parent_parser)
    add_createshipment_parser(subparsers, parent_parser)
    add_updateShipmentStatus_parser(subparsers, parent_parser)
    add_deleteShipment_parser(subparsers, parent_parser)
    add_list_parser(subparsers, parent_parser)
    add_show_parser(subparsers, parent_parser)    

    return parser


def do_createBox(args):
    medicineName = args.medicineName
    medicineID = args.medicineID
    units = args.units

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = TransferClient(base_url = url, keyfile= keyfile)

    if args.wait and args.wait > 0:
        response = client.createBox(
            medicineName,
            medicineID,
            units,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password            
        )
    else:
        response = client.createBox(
            medicineName,
            medicineID,
            units,
            auth_user = auth_user,
            auth_password = auth_password            
        )

    print("Response : {}".format(response))
    

def do_updateBox(args):
    medicineName = args.medicineName
    medicineID = args.medicineID
    units = args.units
    boxID = args.boxID

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = TransferClient(base_url = url, keyfile= keyfile)

    if args.wait and args.wait > 0:
        response = client.updateBox(
            medicineName,
            medicineID,
            units,
            boxID,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password            
        )
    else:
        response = client.updateBox(
            medicineName,
            medicineID,
            units,
            boxID,
            auth_user = auth_user,
            auth_password = auth_password                    
           )

    print("Response : {}".format(response))


def do_createShipment(args):
    boxIDArray = []
    li = args.boxIDArray.split(",")
    for x in li:
        boxIDArray.append(int(x))
    
    origin = args.origin
    destination = args.destination

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = TransferClient(base_url = url, keyfile= keyfile)

    if args.wait and args.wait > 0:
        response = client.createShipment(
            boxIDArray,
            origin,
            destination,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password            
        )
    else:
        response = client.createShipment(
            boxIDArray,
            origin,
            destination,
            auth_user = auth_user,
            auth_password = auth_password            
        )        

    print("Response : {}".format(response))


def do_updateShipmentStatus(args):
    shipmentID = args.shipmentID
    shipmentStatus = args.shipmentStatus

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = TransferClient(base_url = url, keyfile= keyfile)

    if args.wait and args.wait > 0:
        response = client.updateShipmentStatus(
            shipmentID,
            shipmentStatus,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password             
        )
    else:
        response = client.updateShipmentStatus(
            shipmentID,
            shipmentStatus,
            auth_user = auth_user,
            auth_password = auth_password             
        )

    print("Response : {}".format(response))


def do_deleteShipment(args):
    shipmentID = args.shipmentID

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user , auth_password = _get_auth_info(args)

    client = TransferClient(base_url = url, keyfile= keyfile)

    if args.wait and args.wait > 0:
        response = client.deleteShipment(
            shipmentID,
            wait = args.wait,
            auth_user = auth_user,
            auth_password = auth_password
        )
    else:
        response = client.deleteShipment(
            shipmentID,
            auth_user = auth_user,
            auth_password = auth_password
        )        

    print("Response : {}".format(response))


def do_list(args):
    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)

    client = TransferClient(base_url=url, keyfile=None)

    asset_list = [
        asset.split(',')
        for assets in client.list(auth_user=auth_user,auth_password=auth_password)
        for asset in assets.decode().split('|')
    ]

    if asset_list is not None:
        print(asset_list)

    else:
        raise TransferException("Could not retireve List")


def do_show(args):
    ID = args.ID

    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)

    client = TransferClient(base_url=url, keyfile=None)

    data = client.show(ID, auth_user=auth_user, auth_password=auth_password)

    if data is not None:
        print(data)
    else:
        raise TransferException("Asset not found: {}".format(shipmentID))


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
        
    elif args.command == 'updateShipmentStatus':
        do_updateShipmentStatus(args)

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
