class AppointmentFields():
    __configure_appoinments__ = []

    def get_appointment_fields(self, userId):
        configure_appointment = list(filter(lambda x: x["userId"] == userId, self.__configure_appoinment__))
        return configure_appointment
    
    def set_appointment_fields(self, userId, fields):
        fields['userId'] = userId
        self.__configure_appoinment__.append(fields)
        return fields
