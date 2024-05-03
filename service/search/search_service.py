from fuzzywuzzy import fuzz # type: ignore
from service.auth.models import User
from service.appointments.appointments_service import AppointmentsService
from service.configure_appointments.configure_appointments_service import ConfigureAppointmentsService
from service.appointments.appointments_service import AppointmentsService

class SearchService:
    @staticmethod
    def search_service(search_term):
        results = []
        users = [vars(user) for user in User.query.all()]
        
        # Iterate over each user
        for user in users:
            # Iterate over each key-value pair in the user dictionary
            for key, value in user.items():
                # Check if the value is a string and has a partial match with the search term
                if isinstance(value, str) and fuzz.partial_ratio(search_term, value) >= 67:
                    # Remove unnecessary keys from the user dictionary
                    if '_sa_instance_state' in user:
                        user.pop('_sa_instance_state')
                    user.pop('password')
                    # Add the user to the results list
                    results.append(user)
                    break   
        
        new_results = []
        if len(results) > 0:
            # Process each result
            for result in results:
                # Get today's date
                today = AppointmentsService.get_formatted_date()
                # Get appointments for the user
                appointments = AppointmentsService.appointments(result['id'])
                
                if len(appointments) > 0:
                    # Filter appointments for today
                    today_appointments = list(filter(lambda x: x['date'] == today, appointments))
                    if len(today_appointments) > 0:
                        len_appointments = len(today_appointments[0]['appointments'])
                        # Update the result with appointments and fields information
                        SearchService.__appointments_and_fields(result=result, len_appointments=len_appointments)
                    else:
                        # Update the result with fields information for existing user
                        SearchService.__appointments_and_fields(result=result)
                else:
                    # Update the result with fields information for new user
                    # this handles when no appointments have been created yet
                    # which will return no array for new user
                    SearchService.__appointments_and_fields(result=result)
                # Add the updated result to the new_results list
                new_results.append(result)
            return new_results
    
    @staticmethod    
    def __appointments_and_fields(result, len_appointments=0):
        # Update the result with the number of appointments
        result['appointments'] = len_appointments
        # Get appointment fields for the user
        result['fields'] = ConfigureAppointmentsService.get_appointment_fields(result['id'])
