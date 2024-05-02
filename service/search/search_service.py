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
        
        # Iterate through the search data
        for user in users:
            for key, value in user.items():
                # Check if the value is a string and has a partial match with the search term
                if isinstance(value, str) and fuzz.partial_ratio(search_term, value) >= 67:
                    if(user['_sa_instance_state']):
                        user.pop('_sa_instance_state')
                    user.pop('password')
                    results.append(user)
                    break   
        
        new_results = []
        if len(results) > 0:
            for result in results:
                today = AppointmentsService.get_formatted_date()  # Get today's date
                
                # Get the appointments for the current result
                appointments = AppointmentsService.appointments(result['id'])
                
                # Filter appointments that match today's date
                if len(appointments) > 0:
                    today_appointments = list(filter(lambda x: x['date'] == today, appointments))
                    
                    if len(today_appointments) > 0:
                        # Get the number of appointments for today
                        len_appointments = len(today_appointments[0]['appointments'])
                        result['appointments'] = len_appointments
                        result['fields'] = ConfigureAppointmentsService.get_appointment_fields(result['id'])
                    else:
                        # No appointments for today
                        result['appointments'] = 0
                        result['fields'] = ConfigureAppointmentsService.get_appointment_fields(result['id'])
                new_results.append(result)
        return new_results