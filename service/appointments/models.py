class AppointmentsModel():
    __appointments__ = []

    def get_appoinments(self):
        return self.__appointments__
    def add_appointment(self, appointment):
        self.__appointments__.append(appointment)
        return "success"