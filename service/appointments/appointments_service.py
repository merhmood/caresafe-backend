from service.appointments.models import AppointmentsModel

class AppointmentsService():
    @staticmethod
    def add(userId, appointment):
        new_appointment = appointment
        new_appointment['userId'] = userId
        AppointmentsModel().add_appointment(new_appointment)
        return 'appointment added successfully'
    
    @staticmethod
    def appointments(userId):
        appointments = list(filter(lambda x: x["userId"] == userId, AppointmentsModel().get_appoinments()))
        print(appointments)
        return appointments