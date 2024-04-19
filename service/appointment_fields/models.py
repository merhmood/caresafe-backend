class AppointmentFields():
    __fields__ = []
    def get_fields(self):
        return self.__fields__
    def add_field(self, field):
        self.__fields__.append(field)
        return "success"
    