class MedPayload:

    def __init__(self , payload):
        try:
            name, action, newOwner = payload.decode().split(",")

            except ValueError:
                raise InvalidTransaction("Invalid payload serialization")

            if not name:
                raise InvalidTransaction('Name is required')

            if not action:
                raise InvalidTransaction('Action is required')

            if action not in ('createMedicine','updateMedicine','updateMedicineOwner','deleteMedicine'):
                raise InvalidTransaction('Invalid action: {}'.format(action))

            if action == 'updateMedicineOwner':
                newOwner = str(newOwner)
            self._name = name
            self._action = action
            self._newOwner = newOwner

        @staticmethod
        def from_bytes(payload):
            return(MedPayload(payload = payload))


        @property
        def name(self):
            return(self._name)

        @property
        def action(self):
            return(self._action)

        @property
        def newOwner(self):
            return(self._newOwner)
