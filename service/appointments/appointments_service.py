from service.appointments.models import AppointmentsModel

class AppointmentsService():
    @staticmethod
    def add(userId, appointment):
        AppointmentsModel().add_appointment(userId, appointment)
        return 'appointment added successfully'
    
    @staticmethod
    def configure(userId, fields):
        AppointmentsModel().configure_appointment(userId, fields)
        return 'fields successfully configured'
    
    @staticmethod
    def appointments(userId):
        return AppointmentsModel().get_appoinments(userId)