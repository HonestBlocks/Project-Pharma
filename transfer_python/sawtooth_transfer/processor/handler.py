import logging
import datetime

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

LOGGER = logging.getLogger(__name__)

class TransferHandler(TransactionHandler):

    @property
    def family_name(self):
        return('transfer')
    
    @property
    def family_versions(self):
        return(['1.0'])
    
    @property
    def namespaces(self):
        return([TRANSFER_NAMESPACE])
    
    def apply(self, transaction, context):

        header = transaction.header
        signer = header.signer_public_key

        transfer_payload = TransferPayload.from_bytes(transaction.payload)

        transfer_state = TransferState(context)

        if transfer_payload.action == 'createBox':
            if transfer_state.get_box(transfer_payload.boxID) is not None:
                raise InvalidTransaction('Invalid action: BOX already exists')
            
            transfer_state.set_box(transfer_payload.boxID , box)
            _display('Manufacturer: {} created box'.format(signer[:6]))



        elif(transfer_payload.action == 'updateBox'):
            box = transfer_state.get_box(transfer_payload.boxID)


        
        elif(transfer_payload.action == 'createShipment'):
            if transfer_state.get_shipment(transfer_payload.shipmentID) is not None:
                raise InvalidTransaction('Invalid action: Shipment already exists')





        elif(transfer_payload.action == 'updateShipmentStatus'):
            shipment = transfer_state.get_shipment(transfer_payload.shipmentID)
        



        elif(transfer_payload.action == 'deleteShipment'):
            shipment = transfer_state.get_shipment(transfer_payload.shipmentID)

            if shipment is None:
                raise InvalidTransaction('Invalid action : Shipment does not exists: {}'.format(transfer_payload.shipmentID))
            
            if(signer == shipment.logisticsID):
                transfer_state.delete_shipment(transfer_payload.shipmentID)
                _display('Shipment Deleted successfully deleted successfully by: {}'.format(signer[:6]))
            else:
                raise InvalidTransaction('Invalid action UNAUTHORISED ACTION')


        
        else:
            raise InvalidTransaction('Unhandled action: {}'.format(transfer_payload.action))



def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
