from service.routes import db
from service.configure_appointments.models import ConfigureAppointments


class ConfigureAppointmentsService():

    @staticmethod
    def get_appointment_fields(user_id):
        # Retrieve the ConfigureAppointmentsModel for the user
        config = ConfigureAppointments.query.filter_by(user_id=user_id).first()

        # If the config exists, return the appointment_fields
        if config is not None:
            return config.appointment_fields

        # If the config doesn't exist, return an empty list
        return []
    
    @staticmethod
    def set_appointment_fields(user_id, fields):
        # Retrieve the ConfigureAppointmentsModel for the user
        config = ConfigureAppointments.query.filter_by(user_id=user_id).first()

        # If the config doesn't exist, create a new one
        if config is None:
            config = ConfigureAppointments(user_id=user_id, appointment_fields=fields)
            db.session.add(config)
        else:
            # If the config exists, update the appointment_fields
            config.appointment_fields = fields

        # Commit the changes to the database
        db.session.commit()
