MED_NAMESPACE = hashlib.sha512('med'.encode("utf-8")).hexdigest()[0:6]

class Medicine:

    def __init__(self, medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, manufacturerID, owner):
        self.medicineName = medicineName
        self.medicineID = medicineID
        self.medicineKeyContent = medicineKeyContent
        self.medicineAllContents = medicineAllContents
        self.manufactureDate = manufactureDate
        self.expiryDate = expiryDate
        self.manufacturerID = manufacturerID
        self.owner = owner


class MedState:
    TIMEOUT = 5


    def __init__(self, context):
        self._context = context
        self._address_cache = {}



    def delete_medicine(self, medicineName):
        medicines = self._load_medicines(medicineName = medicineName)
        del medicines[medicineName]
        if medicines:
            self._store_medicine(medicineName, medicines = medicines)
        else:
            self._delete_medicine(medicineName)



    def set_medicine(self, medicineName , medicine):
        medicines = self._load_medicines(medicineName = medicineName)
        medicines[medicineName] = medicine
        self._store_medicine(medicineName , medicines = medicines)



    def get_medicine(self , medicineName):
        return(self._load_medicines(medicineName = medicineName).get(medicineName))



    def _store_medicine(self , medicineName , medicines):
        address = _make_medicine_address(medicineName)
        state_data = self.serialize(medicines)
        self._address_cache[address] = state_data
        self._context.set_state({address: state_data} , timeout = self.TIMEOUT)



    def _delete_medicine(self , medicineName):
        address = _make_medicine_address(medicineName)
        self._context.delete_state([address],timeout=self.TIMEOUT)
        self._address_cache[address] = None



    def _load_medicines(self , medicineName):
        address = _make_medicine_address(medicineName)
        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_medicines = self._address_cache[address]
                medicines = self._deserialize(serialized_medicines)
            else:
                games = {}
        else:
            state_entries = self._context.get_state([address],timeout=self.TIMEOUT)
            if state_entries:
                self._address_cache[address] = state_entries[0].data
                medicines = self._deserialize(data=state_entries[0].data)
            else:
                self._address_cache[address] = None
                medicines = {}

        return medicines



    def _deserialize(self , data):
        medicines = {}
        try:
            for medicine in data.decode().split("|"):
                 medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, manufacturerID, owner = medicine.split(",")
                 medicines[medicineName] = Medicine( medicineName, medicineID, medicineKeyContent, medicineAllContents, manufactureDate, expiryDate, manufacturerID, owner)
        except ValueError:
            raise InternalError("Failed to de-serialize medicine data")
        return medicines



    def _serialize(self , medicines):
        med_strs = []
        for medicineName , m in medicines.items():
            med_str = ",".join(medicineName, m.medicineID, m.medicineKeyContent, m.medicineAllContents, m.manufactureDate, m.expiryDate, m.manufacturerID, m.owner)
            med_strs.append(med_str)
        return "|".join(sorted(med_strs)).encode()



    def _make_medicine_address(medicineName):
        return(MED_NAMESPACE+hashlib.sha512(medicineName.encode('utf-8')).hexdigest()[:64])
