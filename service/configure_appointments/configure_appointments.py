from service.configure_appointments.models import ConfigureAppointmentsModel
class ConfigureAppointments():

    @staticmethod
    def get_appointment_fields(userId):
        # Get all fields from the model
        fields = ConfigureAppointmentsModel().get_fields()
        
        # Filter the fields to get only the ones belonging to the user
        user_fields = list(filter(lambda x: x["id"] == userId, fields))
        
        # Get the latest user field
        user_field = user_fields[len(user_fields)-1]
        
        result = []
        
        # Convert the user_field to a list
        for key in user_field:
            # Add the value to the result list
            result.append(user_field[key])
        
        # Remove the id field from the result list
        result.pop()
        
        return result
    
    @staticmethod
    def set_appointment_fields(userId, fields):
        # Remove any existing field for the user
        ConfigureAppointmentsModel().remove_field(userId)
        
        new_field = {}
        
        # Create a new field dictionary with the given fields
        for field in fields:
            new_field[field] = field
        
        # Set the id field for the user
        new_field['id'] = userId
        
        # Add the new field to the model
        ConfigureAppointmentsModel().add_field(new_field)
        
        # Remove the "userId" key from the new_field dictionary
        if "userId" in new_field:
           new_field.pop("userId")
        
        return "success"
