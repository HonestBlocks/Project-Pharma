from __future__ import print_function

import os
import subprocess

from setuptools import setup, find_packages

conf_dir = "/etc/sawtooth"

data_files = [
    (conf_dir, ['packaging/med.toml.example'])
]

if os.path.exists("/etc/default"):
    data_files.append(
        ('/etc/default', ['packaging/systemd/sawtooth-med-tp-python']))

if os.path.exists("/lib/systemd/system"):
    data_files.append(('/lib/systemd/system',
                       ['packaging/systemd/sawtooth-med-tp-python.service']))

setup(
    name='sawtooth-med',
    version=subprocess.check_output(
        ['../../bin/get_version']).decode('utf-8').strip(),
    description='Sawtooth Med',
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
            'med = sawtooth_med.med_cli:main_wrapper',
            'med-tp-python = sawtooth_med.processor.main:main',
        ]
    })
