from datetime import datetime
from itertools import groupby
from  service.routes import db
from service.appointments.models import Appointments
from service.profile.profile_service import ProfileService

class AppointmentsService():
    @staticmethod
    def add(user_id, appointment, role):
        """
        Adds a new appointment for a given user.

        Args:
            userId (int): The ID of the user.
            appointment (dict): The appointment details.

        Returns:
            str: A success message indicating that the appointment was added successfully.
        """
        
        todaysDate = AppointmentsService.get_formatted_date()

        threshold = ProfileService.get_threshold(user_id=user_id)
        appointments = Appointments.query.filter_by(user_id = user_id).all()

        todays_appointments = []
        todays_remote_appointments = []

        for item in [appointment.appointments for appointment in appointments]:
            if(item['date'] == todaysDate):
                todays_appointments.append(item['date'])
            if(item['date'] == todaysDate and item['remote'] == True):
                todays_remote_appointments.append(item['date'])

        today_appointments_length  = len(todays_appointments)
        today_remote_appointments_length = len(todays_remote_appointments)

        # Checks if the daily appointment threshold has been reached
        if(today_appointments_length  == int(threshold['dailyAppointmentsThreshold'])):
            return {'dailyAppointmentsThreshold': 'reached'}
        # Checks if the remote threhold has been reached
        elif(
            today_appointments_length > today_remote_appointments_length and 
            today_remote_appointments_length == int(threshold['remoteAppointmentsThreshold']) and 
            role != 'businessUser'
        ):
            return {'remoteAppointmentsThreshold': 'reached'}
        else:
            print('appointment add')
            # Get the formatted date
            appointment['date'] = todaysDate

            if(role != 'businessUser'):
                appointment['remote'] = True
            else:
                appointment['remote'] = False
            # Create a new Appointment object and add it to the database
            new_appointment = Appointments(user_id=user_id, appointments=appointment)
            db.session.add(new_appointment)
            db.session.commit()
            
            # Return success message
            return {'appointment': 'appointment added successfully'}
    @staticmethod
    def appointments(user_id):
        """
        Retrieve and organize appointments for a specific user.

        Args:
            userId (int): The ID of the user.

        Returns:
            list: A list of dictionaries representing grouped appointments, sorted by date in descending order.

        Example:
            >>> appointments(123)
            [
                {
                    'date': '2022-01-01',
                    'appointments': [
                        {'id': 1, 'userId': 123, 'date': '2022-01-01', 'time': '09:00'},
                        {'id': 2, 'userId': 123, 'date': '2022-01-01', 'time': '10:00'}
                    ]
                },
                {
                    'date': '2022-01-02',
                    'appointments': [
                        {'id': 3, 'userId': 123, 'date': '2022-01-02', 'time': '14:00'}
                    ]
                }
            ]
        """
       # Query the database for appointments for the user
        appointments = Appointments.query.filter_by(user_id=user_id).all()

        # Convert the appointments to a list of dictionaries
        appointments = [appointment.appointments for appointment in appointments]


        # Group appointments by date
        grouped_appointments = []
        for date, group in groupby(appointments, key=lambda x: x['date']):
            grouped_appointments.append({'date': date, 'appointments': list(group)})
        
        # Reverse the order of appointments within each group
        reversed_grouped_appointments = []
        for group_appointment in grouped_appointments:
            group_appointment["appointments"].reverse()
            reversed_grouped_appointments.append(group_appointment)
 
        # Return reversed grouped appointments
        reversed_grouped_appointments.reverse()
        return reversed_grouped_appointments
    
    @staticmethod
    def get_formatted_date():
        """
        Get the current date and format it as a string.

        Returns:
            str: The formatted date string in the format "day Month, Year".
        """
        # Get current date and time
        now = datetime.now()
        
        # Get day, month, and year
        day = now.strftime("%d")
        month = now.strftime("%b")
        year = now.strftime("%Y")
        
        # Determine the suffix for the day
        suffix = "th" if 11 <= int(day) <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(int(day) % 10, "th")
        
        # Format the date
        formatted_date = f"{day}{suffix} {month}, {year}"
        
        # Return the formatted date
        return formatted_date
