from __future__ import print_function

import os
import subprocess

from setuptools import setup, find_packages

conf_dir = "/etc/sawtooth"

data_files = [
    (conf_dir, ['packaging/transfer.toml.example'])
]

if os.path.exists("/etc/default"):
    data_files.append(
        ('/etc/default', ['packaging/systemd/sawtooth-transfer-tp-python']))

if os.path.exists("/lib/systemd/system"):
    data_files.append(('/lib/systemd/system',
                       ['packaging/systemd/sawtooth-transfer-tp-python.service']))

setup(
    name='sawtooth-transfer',
    version=subprocess.check_output(
        ['../../bin/get_version']).decode('utf-8').strip(),
    description='Sawtooth TRANSFER',
    author='Hyperledger Sawtooth',
    url='https://github.com/hyperledger/sawtooth-sdk-python',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'PyYAML',
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'transfer = sawtooth_transfer.transfer_cli:main_wrapper',
            'transfer-tp-python = sawtooth_transfer.processor.main:main',
        ]
    })
