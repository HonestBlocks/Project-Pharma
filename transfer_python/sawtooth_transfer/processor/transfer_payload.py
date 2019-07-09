import hashlib
import base64

from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

class TransferPayload:

    def __init__(self, payload):
        try:
            medicineName, medicineID , units, originAdd, destinationAdd, boxID, logisticsID, shipmentID, boxIDArray, shipmentStatus , action = payload.decode().split(",")

            except ValueError:
                raise InvalidTransaction("Invalid payload serialization")
        
        if not action:
            raise InvalidTransaction('Action required')

        if action not in ('createBox', 'updateBox', 'createShipment', 'updateShipmentStatus', 'deleteShipment'):
            raise InvalidTransaction('Invalid Action : {}'.format(action))
        


        self._medicineName = medicineName
        self._medicineID = medicineID
        self._units = units
        self._originAdd = originAdd
        self._destinationAdd = destinationAdd
        self._boxID = boxID
        self._logisticsID = logisticsID
        self._shipmentID = shipmentID
        self._boxIDArray = boxIDArray
        self._shipmentStatus = shipmentStatus
        self._action = action

    
    @staticmethod
    def from_bytes(payload):
        return(TransferPayload(payload = payload))
    
    @property
    def medicineName(self):
        return(self._medicineName)

    @property
    def medicineID(self):
        return(self._medicineID)
    
    @property
    def units(self):
        return(self._units)

    @property
    def originAdd(self):
        return(self._originAdd)

    @property
    def destinationAdd(self):
        return(self._destinationAdd)

    @property
    def boxID(self):
        return(self._boxID)

    @property
    def logisticsID(self):
        return(self._logisticsID)

    @property
    def shipmentID(self):
        return(self._shipmentID)

    @property
    def shipmentStatus(self):
        return(self._shipmentStatus)

    @property
    def action(self):
        return(self._action)

    @property
    def boxIDArray(self):
        return(self._boxIDArray)