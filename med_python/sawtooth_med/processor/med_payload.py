import hashlib
import base64

from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

class MedPayload:

    def __init__(self , payload):
        try:
            medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, stock, manufacturerID , action , newOwner= payload.decode().split(",")

        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        if not medicineName:
            raise InvalidTransaction('Medicine Name is required')

        if not action:
            raise InvalidTransaction('Action is required')

        if action not in ('createMedicine','updateMedicine','updateMedicineOwner','deleteMedicine', 'produce'):
            raise InvalidTransaction('Invalid action: {}'.format(action))

        if action == 'updateMedicineOwner':
            newOwner = str(newOwner)


        self._medicineName = medicineName
        self._medicineID = medicineID
        self._medicineKeyContent = medicineKeyContent
        self._medicineAllContents = medicineAllContents
        self._manufactureDate = manufactureDate
        self._expiryDate = expiryDate
        self._stock = stock
        self._manufacturerID = manufacturerID
        self._action = action
        self._newOwner = newOwner

    @staticmethod
    def from_bytes(payload):
        return(MedPayload(payload = payload))


    @property
    def medicineName(self):
        return(self._medicineName)

    @property
    def medicineID(self):
        return(self._medicineID)

    @property
    def medicineKeyContent(self):
        return(self._medicineKeyContent)

    @property
    def medicineAllContents(self):
        return(self._medicineAllContents)

    @property
    def manufactureDate(self):
        return(self._manufactureDate)

    @property
    def expiryDate(self):
        return(self._expiryDate)

    @property
    def manufacturerID(self):
        return(self._manufacturerID)

    @property
    def action(self):
        return(self._action)

    @property
    def newOwner(self):
        return(self._newOwner)

    @property
    def stock(self):
        return(self._stock)
