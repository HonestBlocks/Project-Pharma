import os
from hashlib import sha512
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from dotenv import load_dotenv

MED_NAMESPACE = hashlib.sha512('med'.encode("utf-8")).hexdigest()[0:6]

load_dotenv()

txn_header_bytes = TransactionHeader(
    family_name='med',
    family_version='1.0',
    inputs=[MED_NAMESPACE],
    outputs=[MED_NAMESPACE]
    signer_public_key= os.getenv("PUBLIC_KEY"),

    batcher_public_key= os.getenv("PUBLIC_KEY"),

    dependencies=[],
    payload_sha512=sha512(payload_bytes).hexdigest()
).SerializeToString()


signature = signer.sign(txn_header_bytes)

txn = Transaction(
    header=txn_header_bytes,
    header_signature=signature,
    payload=payload_bytes
)
