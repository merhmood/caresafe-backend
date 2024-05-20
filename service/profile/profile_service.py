from .models import Profile
from service.routes import db


class ProfileService():
    @staticmethod
    def get_profile_details(user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile is not None:
            return {
                'imgUrl': profile.img_url, 
                'name': profile.name, 
                'address': profile.address, 
                'remoteAppointmentsThreshold': profile.remote_appointments_threshold, 
                'dailyAppointmentsThreshold': profile.daily_appointments_threshold
            }
        return {}
    
    def create_profile(user_id, name, address):
        new_profile = Profile(user_id=user_id, name=name, address=address, daily_appointments_threshold=100, remote_appointments_threshold=20)
        db.session.add(new_profile)
        db.session.commit()

    def update_profile_details(user_id, new_profile_details):
        print(new_profile_details)
        profile = Profile.query.filter_by(user_id=user_id).first()
        profile.name = new_profile_details['name']
        profile.address = new_profile_details['address']
        profile.daily_appointments_threshold = new_profile_details['dailyAppointmentsThreshold']
        profile.remote_appointments_threshold = new_profile_details['remoteAppointmentsThreshold']

        db.session.commit()
        return {'message': 'profile updated'}