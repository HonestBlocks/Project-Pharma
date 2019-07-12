import logging
import datetime

from sawtooth_transfer.processor.transfer_payload import TransferPayload
from sawtooth_transfer.processor.transfer_state import Box
from sawtooth_transfer.processor.transfer_state import Shipment
from sawtooth_transfer.processor.transfer_state import Medicine
from sawtooth_transfer.processor.transfer_state import TransferState
from sawtooth_transfer.processor.transfer_state import TRANSFER_NAMESPACE
from sawtooth_transfer.processor.transfer_state import MED_NAMESPACE

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

            medicine = transfer_state.get_medicine(transfer_payload.medicineName)
            if medicine:
                if( int(medicine.stock) >= int(transfer_payload.units)):
                    medicine.stock = str(int(medicine.stock) - int(transfer_payload.units))
                    transfer_state.set_medicine(transfer_payload.medicineName , medicine)
                    box = Box(
                        medicineName = transfer_payload.medicineName,
                        medicineID = transfer_payload.medicineID,
                        units = transfer_payload.units,
                        boxID = transfer_payload.boxID
                    )
                    transfer_state.set_box(transfer_payload.boxID , box)
                    _display('Manufacturer: {} created box'.format(signer[:6]))
                else:
                    raise InvalidTransaction('Number of units assigned are greater than stocks left!')
            else:
                raise InvalidTransaction('NO such medicine present to PACK!')



        elif(transfer_payload.action == 'updateBox'):
            box = transfer_state.get_box(transfer_payload.boxID)

            if box:
                medicine = transfer_state.get_medicine(transfer_payload.medicineName)
                if medicine:
                    if(int(medicine.stock) >= int(transfer_payload.units)):
                        medicine.stock = str(int(medicine.stock) - int(transfer_payload.units))
                        transfer_state.set_medicine(transfer_payload.medicineName , medicine)
                        box = Box(
                            medicineName = transfer_payload.medicineName,
                            medicineID = transfer_payload.medicineID,
                            units = transfer_payload.units,
                            boxID = transfer_payload.boxID
                        )
                        transfer_state.set_box(transfer_payload.boxID , box)
                        _display('Manufacturer: {} created box'.format(signer[:6]))
                    else:
                        raise InvalidTransaction('Number of units assigned are greater than stocks left!')
                else:
                    raise InvalidTransaction('Invalid action: NO SUCH medicine')  
            
            else:
                raise InvalidTransaction('Invalid action: NO SUCH BOX')


        
        elif(transfer_payload.action == 'createShipment'):
            if transfer_state.get_shipment(transfer_payload.shipmentID) is not None:
                raise InvalidTransaction('Invalid action: Shipment already exists')
            

            shipment = Shipment(
                    shipmentID = transfer_payload.shipmentID,
                    logisticsID = transfer_payload.logisticsID,
                    boxIDArray = transfer_payload.boxIDArray,
                    originAdd = transfer_payload.origin,
                    destinationAdd = transfer_payload.destinationAdd,
                    shipmentStatus = transfer_payload.shipmentStatus
            )

            transfer_state.set_shipment(transfer_payload.shipmentID , shipment)
            _display('Logistics Company : {} created Shipment'.format(signer[:6]))



        elif(transfer_payload.action == 'updateShipmentStatus'):
            shipment = transfer_state.get_shipment(transfer_payload.shipmentID)

            shipment.shipmentStatus = transfer_payload.shipmentStatus
            transfer_state.set_shipment(transfer_payload.shipmentID , shipment)
            _display('Logistics Company : {} created Shipment'.format(signer[:6]))



        elif(transfer_payload.action == 'deleteShipment'):
            shipment = transfer_state.get_shipment(transfer_payload.shipmentID)

            if shipment is None:
                raise InvalidTransaction('Invalid action : Shipment does not exists: {}'.format(transfer_payload.shipmentID))
            
            if(signer == shipment.logisticsID) and (shipment.shipmentStatus == shipment.destinationAdd):
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
