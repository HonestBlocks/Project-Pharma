
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

from sawtooth_PharmaChain.processor.handler import Medicine


def main():
    processor = TransactionProcessor(url = 'tcp://127.0.0.1:4004')
    medHandler = Medicine()
    processor.add_handler(medHandler)
    processor.start()
