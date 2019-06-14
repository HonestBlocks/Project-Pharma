from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_PharmaChain.processor.handler import Medicine


def main():
    processor = TransactionProcessor(url = 'tcp://127.0.0.1:4004')
    medHandler = Medicine()
    processor.add_handler(medHandler)
    processor.start()
