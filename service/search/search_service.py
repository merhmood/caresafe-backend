from fuzzywuzzy import fuzz # type: ignore
from service.search.models import SearchModel
from service.appointments.appointments_service import AppointmentsService
from service.configure_appointments.configure_appointments import ConfigureAppointments
from service.appointments.appointments_service import AppointmentsService

class SearchService:
    @staticmethod
    def search_service(search_term):
        results = []
        
        # Iterate through the search data
        for item in SearchModel().get_search_data():
            for key, value in item.items():
                # Check if the value is a string and has a partial match with the search term
                if isinstance(value, str) and fuzz.partial_ratio(search_term, value) >= 67:
                    results.append(item)
                    break
        
        print("search results")
        print(results)
        
        new_results = []
        
        if len(results) > 0:
            for result in results:
                today = AppointmentsService.get_formatted_date()  # Get today's date
                
                # Get the appointments for the current result
                appointments = AppointmentsService.appointments(result['id'])
                print(appointments)
                
                # Filter appointments that match today's date
                if len(appointments) > 0:
                    today_appointments = list(filter(lambda x: x['date'] == today, appointments))[0]
                    len_appointments = len(today_appointments["appointments"])
                    result['appointments'] = len_appointments
                    result['fields'] = ConfigureAppointments().get_appointment_fields(result['id'])
                else:
                    result['appointments'] = 0
                    result['fields'] = ConfigureAppointments().get_appointment_fields(result['id'])
                
                new_results.append(result)
            
            print(new_results)
        
        return new_results