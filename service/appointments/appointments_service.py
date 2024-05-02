from datetime import datetime
from itertools import groupby
from  service.routes import db
from service.appointments.models import Appointments

class AppointmentsService():
    @staticmethod
    def add(userId, appointment):
        """
        Adds a new appointment for a given user.

        Args:
            userId (int): The ID of the user.
            appointment (dict): The appointment details.

        Returns:
            str: A success message indicating that the appointment was added successfully.
        """
        
        # Get the formatted date
        appointment['date'] = AppointmentsService.get_formatted_date()
        
        # Create a new Appointment object and add it to the database
        new_appointment = Appointments(user_id=userId, appointments=appointment)
        db.session.add(new_appointment)
        db.session.commit()
        
        # Return success message
        return 'appointment added successfully'
    
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
        
        # Sort appointments by date
        appointments.sort(key=lambda x: x['date'])
        
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
