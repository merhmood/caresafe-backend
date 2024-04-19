class AppointmentsModel():
    __appointments__ = []
    __configure_appoinment__ = []

    def get_appoinments(self, userId):
        userAppointments = list(filter(lambda x: x["userId"] == userId, self.__appointments__))
        return userAppointments
    def add_appointment(self, userId, appointment):
        appointment['userId'] = userId
        self.__appointments__.append(appointment)
        return appointment
    def configure_appointment(self, userId, fields):
        # fields["id"] is the userId
        user_configured_appointment = len(list(filter(lambda x: x["userId"] == userId, self.__configure_appoinment__)))
        if( user_configured_appointment == 0 ):
            fields["id"] = userId
            self.__configure_appoinment__.append(fields)
            result = []
            for key in new_fields:
                result.append(key)
            return result
        else:
            new_fields = {}
            fields = list(filter(lambda x: x["userId"] == userId, self.__configure_appoinment__))[0]
            for key in fields:
                new_fields[key] = fields[key]
            new_fields['id'] = userId
            self.__configure_appoinment__.append( new_fields)
            result = []
            for key in new_fields:
                result.append(key)
            return result