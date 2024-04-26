from datetime import datetime
from itertools import groupby
from service.appointments.models import AppointmentsModel

class AppointmentsService():
    @staticmethod
    def add(userId, appointment):
        # Add userId to the appointment
        appointment['userId'] = userId
        
        # Get the formatted date
        appointment['date'] = AppointmentsService.get_formatted_date()
        
        # Add the appointment to the AppointmentsModel
        AppointmentsModel().add_appointment(appointment)
        
        # Return success message
        return 'appointment added successfully'
    
    @staticmethod
    def appointments(userId):
        # Get all appointments
        appointments = AppointmentsModel().get_appoinments()
        
        # Filter appointments by userId
        appointments = [appointment for appointment in appointments if appointment["userId"] == userId]
        
        # Sort appointments by date
        appointments.sort(key=lambda x: x['date'])
        
        # Group appointments by date
        grouped_appointments = []
        for date, group in groupby(appointments, key=lambda x: x['date']):
            grouped_appointments.append({'date': date, 'appointments': list(group)})
        
        # Return grouped appointments
        return grouped_appointments
    
    @staticmethod
    def get_formatted_date():
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
