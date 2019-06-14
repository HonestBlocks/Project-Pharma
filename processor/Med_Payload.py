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

            if action == ''
