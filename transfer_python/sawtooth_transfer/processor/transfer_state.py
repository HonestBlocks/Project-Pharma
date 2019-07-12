import hashlib

from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.exceptions import InvalidTransaction

MED_NAMESPACE = hashlib.sha512('med'.encode("utf-8")).hexdigest()[0:6]
TRANSFER_NAMESPACE = hashlib.sha512('transfer'.encode("utf-8")).hexdigest()[0:6]

def _make_medicine_address(medicineName):
    return(MED_NAMESPACE+hashlib.sha512(medicineName.encode('utf-8')).hexdigest()[:64])

def _make_transfer_address(name):
    return(TRANSFER_NAMESPACE+hashlib.sha512(name.encode('utf-8')).hexdigest()[:64])

class Medicine:

    def __init__(self, medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, stock, manufacturerID, owner):
        self.medicineName = medicineName
        self.medicineID = medicineID
        self.medicineKeyContent = medicineKeyContent
        self.medicineAllContents = medicineAllContents
        self.manufactureDate = manufactureDate
        self.expiryDate = expiryDate
        self.stock = stock
        self.manufacturerID = manufacturerID
        self.owner = owner


class Box:

    def __init__(self, medicineName, medicineID, units, boxID):
        self.medicineName = medicineName
        self.medicineID = medicineID
        self.units = units
        self.boxID = boxID


class Shipment:

    def __init__(self, shipmentID, logisticsID, boxIDArray, origin, destination, shipmentStatus):
        self.shipmentID = shipmentID
        self.logisticsID = logisticsID
        self.boxIDArray = boxIDArray
        self.origin = origin
        self.destination = destination
        self.shipmentStatus = shipmentStatus


class TransferState:
    TIMEOUT = 5


    def __init__(self, context):
        self._context = context
        self._address_cache = {}
    

    def _load_medicines(self , medicineName):
        address = _make_medicine_address(medicineName)
        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_medicines = self._address_cache[address]
                fmedicines = self._deserialize(serialized_medicines)
            else:
                fmedicines = {}
        else:
            state_entries = self._context.get_state([address],timeout=self.TIMEOUT)
            if state_entries:
                self._address_cache[address] = state_entries[0].data
                fmedicines = self._deserialize(data=state_entries[0].data)
            else:
                self._address_cache[address] = None
                fmedicines = {}
        return fmedicines



    def _load_boxes(self , boxID):
        address = _make_transfer_address(boxID)
        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_boxes = self._address_cache[address]
                fboxes = self._deserializeb(serialized_boxes)
            else:
                fboxes = {}
        else:
            state_entries = self._context.get_state([address],timeout=self.TIMEOUT)
            if state_entries:
                self._address_cache[address] = state_entries[0].data
                fboxes = self._deserializeb(data=state_entries[0].data)
            else:
                self._address_cache[address] = None
                fboxes = {}

        return fboxes


    def _load_shipments(self , shipmentID):
        address = _make_transfer_address(shipmentID)
        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_shipments = self._address_cache[address]
                fshipments = self._deserializes(serialized_shipments)
            else:
                fshipments = {}
        else:
            state_entries = self._context.get_state([address],timeout=self.TIMEOUT)
            if state_entries:
                self._address_cache[address] = state_entries[0].data
                fshipments = self._deserializes(data=state_entries[0].data)
            else:
                self._address_cache[address] = None
                fshipments = {}

        return fshipments


    def delete_shipment(self, shipmentID):
        shipments = self._load_shipments(shipmentID = shipmentID)
        del shipments[shipmentID]
        if shipments:
            self._store_shipment(shipmentID, shipments = shipments)
        else:
            self._delete_shipment(shipmentID)


    def delete_box(self, boxID):
        boxes = self._load_boxes(boxID = boxID)
        del boxes[boxID]
        if boxes:
            self._store_box(boxID, boxes = boxes)
        else:
            self._delete_box(boxID)


    def delete_medicine(self, medicineName):
        medicines = self._load_medicines(medicineName = medicineName)
        del medicines[medicineName]
        if medicines:
            self._store_medicine(medicineName, medicines = medicines)
        else:
            self._delete_medicine(medicineName)


    def _store_shipment(self , shipmentID , shipments):
        address = _make_transfer_address(shipmentID)
        state_data = self._serializes(shipments)
        self._address_cache[address] = state_data
        self._context.set_state({address: state_data} , timeout = self.TIMEOUT)


    def _store_box(self , boxID , boxes):
        address = _make_transfer_address(boxID)
        state_data = self._serializeb(boxes)
        self._address_cache[address] = state_data
        self._context.set_state({address: state_data} , timeout = self.TIMEOUT)


    def _store_medicine(self , medicineName , medicines):
        address = _make_medicine_address(medicineName)
        state_data = self._serialize(medicines)
        self._address_cache[address] = state_data
        self._context.set_state({address: state_data} , timeout = self.TIMEOUT)

    def set_box(self, boxID , box):
        boxes = self._load_boxes(boxID = boxID)

        boxes[boxID] = box
        self._store_box(boxID , boxes = boxes)

    def set_shipment(self, shipmentID , shipment):
        shipments = self._load_shipments(shipmentID = shipmentID)
        shipments[shipmentID] = shipment
        self._store_shipment(shipmentID , shipments = shipments)
    

    def set_medicine(self, medicineName , medicine):
        medicines = self._load_medicines(medicineName = medicineName)
        medicines[medicineName] = medicine
        self._store_medicine(medicineName , medicines = medicines)


    def _delete_shipment(self , shipmentID):
        address = _make_transfer_address(shipmentID)
        self._context.delete_state([address],timeout=self.TIMEOUT)
        self._address_cache[address] = None


    def _delete_box(self , boxID):
        address = _make_transfer_address(boxID)
        self._context.delete_state([address],timeout=self.TIMEOUT)
        self._address_cache[address] = None


    def _delete_medicine(self , medicineName):
        address = _make_medicine_address(medicineName)
        self._context.delete_state([address],timeout=self.TIMEOUT)
        self._address_cache[address] = None



    def get_medicine(self , medicineName):
        return(self._load_medicines(medicineName = medicineName).get(medicineName))


    def get_box(self , boxID):
        return(self._load_boxes(boxID = boxID).get(boxID))

    def get_shipment(self , shipmentID):
        return(self._load_shipments(shipmentID = shipmentID).get(shipmentID))



    def _deserialize(self , data):
        medicines = {}
        try:
            for medicine in data.decode().split("|"):
                medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, stock, manufacturerID, owner= medicine.split(",")
                medicines[medicineName] = Medicine(medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, stock, manufacturerID, owner)
        except ValueError:
            raise InternalError("Failed to de-serialize medicine data")
        return medicines



    def _deserializes(self , data):
        shipments = {}
        try:
            for shipment in data.decode().split("|"):
                shipmentID, logisticsID, boxIDArray, origin, destination, shipmentStatus = shipment.split(",")
                shipments[shipmentID] = Shipment(shipmentID, logisticsID, boxIDArray, origin, destination, shipmentStatus)
        except ValueError:
            raise InternalError("Failed to de-serialize shipment data")
        return shipments


    def _deserializeb(self , data):

        try:
            boxes = {}
            for box in data.decode().split("|"):
                medicineName, medicineID, units, boxID = box.split(",")
                boxes[boxID] = Box(medicineName, medicineID, units, boxID)
        except ValueError:
            raise InternalError("Failed to de-serialize box data")
        return boxes


    def _serialize(self , medicines):
        med_strs = []
        for medicineName , m in medicines.items():
            med_str = ",".join([medicineName, m.medicineID, m.medicineKeyContent, m.medicineAllContents, m.manufactureDate, m.expiryDate, m.stock ,m.manufacturerID, m.owner])
            med_strs.append(med_str)
        return "|".join(sorted(med_strs)).encode()



    def _serializes(self , shipments):
        shipment_strs = []
        for shipmentID , m in shipments.items():
            shipment_str = ",".join([shipmentID, m.logisticsID, str(m.boxIDArray), m.origin, m.destination, str(m.shipmentStatus)])
            shipment_strs.append(shipment_str)
        return "|".join(sorted(shipment_strs)).encode()


    def _serializeb(self , boxes):
        box_strs = []
        for boxID , m in boxes.items():
            box_str = ",".join([str(m.medicineName), str(m.medicineID), str(m.units), str(boxID)])
            box_strs.append(box_str)
        return "|".join(sorted(box_strs)).encode()
