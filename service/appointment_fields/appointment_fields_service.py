from service.appointment_fields.models import AppointmentFieldsModel

class AppointmentFields():

    @staticmethod
    def get_appointment_fields(userId):
        fields = AppointmentFieldsModel().get_fields()
        user_fields = list(filter(lambda x: x["id"] == userId, fields))
        user_field = user_fields[len(user_fields)-1]
        result = []
        for key in user_field:
            result.append(user_field[key])
        result.pop()
        return result
    
    @staticmethod
    def set_appointment_fields(userId, fields):
        AppointmentFieldsModel().remove_field(userId)
        new_field = {}
        for field in fields:
            new_field[field] = field
        new_field['id'] = userId
        AppointmentFieldsModel().add_field(new_field)
        print(new_field)
        return "success"
