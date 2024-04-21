from fuzzywuzzy import fuzz
from service.search.models import SearchModel
from service.appointments.appointments_service import AppointmentsService
from service.appointment_fields.appointment_fields_service import AppointmentFields

class SearchService:
    @staticmethod
    def search_service(search_term):
        results = []
        for item in SearchModel().get_search_data():
            for key, value in item.items():
                if isinstance(value, str) and fuzz.partial_ratio(search_term, value) >= 67:
                    results.append(item)
                    break
        print("search results")
        new_result = []
        for result in results:
            len_appointments = len(list(filter(lambda x: x['userId'] == result['id'], AppointmentsService.appointments(result['id']))))
            result['appointments'] = len_appointments
            result['fields'] = AppointmentFields().get_appointment_fields(result['id'])
            new_result.append(result)
        print(results)
        return results