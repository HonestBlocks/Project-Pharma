from sawtooth_PharmaChain.processor.Med_Payload import MedPayload
from datetime import datetime

class Medicine(TransactionHandler):

    def __init__(self , namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return('med')

    @property
    def family_versions(self):
        return(['1.0'])

    @property
    def namespaces(self):
        return([self._namespace_prefix])

    def apply(self, transaction , context):
        header = transaction.header
        signer = header.signer_public_key

        med_payload = MedPayload.from_bytes(transaction.payload)

        med_state = MedState(context)

        if med_payload.action == 'createMedicine':
            if med_state.get_state(med_payload.name) is not None:
                raise InvalidTransaction('Invalid action: Medicine already exists: {}'.format(med_payload.name))
        print("-"*49)
        print((" "*17)+"CREATE MEDICINE"+" "*17)
        print("-"*49)
        medicineAllContents = []
        medicineID = input('Enter Medicine ID              :')
        medicineKeyContent = input('Enter Key Content              :')
        medicineAllContentsCount = int(input('Enter All Contents Count       :'))
        for x in range(0,medicineAllContentsCount):
            content = input('Enter Name-Percent')
            medicineAllContents.append(content)
        manufactureDate = datetime.date(datetime.now())
        expirymonths = input('Enter months of expiry from now:')
        expiryDate = (datetime.date.today() + datetime.timedelta(6*365/12))
        manufacturerID = signer
        owner = input('Enter Entity Name             :')
        medicine = Medicine(
                            medicineName = med_payload.name,
                            medicineID = medicineID,
                            medicineKeyContent = medicineKeyContent,
                            medicineAllContents = medicineAllContents,
                            manufactureDate = manufactureDate,
                            expiryDate = expiryDate,
                            manufacturerID = manufacturerID,
                            owner = owner
                                )
        med_state.set_medicine(med_payload.name , medicine)
        _display('Manufacturer: {} created medicine'.format(signer[:6]))




        elif med_payload.action == 'updateMedicine':
            med = med_state.get_medicine(med_payload.name)
            if med:
                if(signer == med.manufacturerID):
                    print("-"*49)
                    print((" "*17)+"UPDATE MEDICINE"+" "*17)
                    print("-"*49)
                    contentcount = input('Enter number of Contents in medicine:')
                    for x in range(0,contentcount):
                        content = input('Enter Name-Percent')
                        med.medicineAllContents.append(content)
                    med_state.set_medicine(med_payload.name , medicine)
                    _display('Manufacturer: {} updated medicine successfully'.format(signer[:6]))
                else:
                    raise InvalidTransaction('Invalid action: UnAUTHORISED ACTION')
            else:
                raise InvalidTransaction('Invalid action: Medicine DOES NOT exists: {}'.format(med_payload.name))


        elif med_payload.action == 'updateMedicineOwner':
            med = med_state.get_medicine(med_payload.name)
            if med:
                if(med_payload.newOwner != med.owner):
                    med.owner = med_payload.newOwner
                    med_state.set_medicine(med_payload.name , medicine)
                    _display('Owner Updated by : {}'.format(signer[:6]))



        elif med_payload.action == 'deleteMedicine':
            medicine = med_state.get_state(med_payload.name)

            if medicine is None:
                raise InvalidTransaction('Invald action: medicine does not exist')

            med_state.delete_medicine(med_payload.name)
            _display('Medecine Info deleted successfully by: {}'.format(signer[:6]))

        else:
            raise InvalidTransaction('Unhandled action: {}'.format(med_payload.action))
