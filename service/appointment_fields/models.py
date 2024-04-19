class AppointmentFieldsModel():
    __fields__ = []
    def get_fields(self):
        return self.__fields__
    def add_field(self, field):
        self.__fields__.append(field)
        return "success"
    def remove_field(self, field):
        if field in self.__fields__:
            self.__fields__.remove(field)
        return "success"
    