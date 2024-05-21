from .models import Profile
from service.routes import db


class ProfileService():
    @staticmethod
    def get_profile_details(user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile is not None:
            return {
                'name': profile.name, 
                'address': profile.address, 
                'remoteAppointmentsThreshold': profile.remote_appointments_threshold, 
                'dailyAppointmentsThreshold': profile.daily_appointments_threshold
            }
        else:
            # Using local import to avoid circular import 
            from service.auth.auth_service import AuthService
            # Create profile if user profile hasn't created profile before
            user = AuthService.get_user(user_id = user_id)
            ProfileService.create_profile(
                user_id=user_id, 
                name = user['name'], 
                address = user['address']
            )
            # Threshold values should match does of create profile
            return {
                'name': user.name, 
                'address': user.address, 
                'remoteAppointmentsThreshold': 20, 
                'dailyAppointmentsThreshold': 100
            }
    
    @staticmethod
    def create_profile(user_id, name, address):
        new_profile = Profile(
            user_id=user_id, 
            name=name, 
            address=address, 
            remote_appointments_threshold=20,
            daily_appointments_threshold=100
        )
        db.session.add(new_profile)
        db.session.commit()

    @staticmethod
    def update_profile_details(user_id, new_profile_details):
        profile = Profile.query.filter_by(user_id=user_id).first()
        profile.name = new_profile_details['name']
        profile.address = new_profile_details['address']
        profile.daily_appointments_threshold = new_profile_details['dailyAppointmentsThreshold']
        profile.remote_appointments_threshold = new_profile_details['remoteAppointmentsThreshold']

        db.session.commit()
        return {'message': 'profile updated'}
    
    @staticmethod
    def get_threshold(user_id):
        profile = Profile.query.filter_by(user_id=user_id).first()
        daily_appointments_threshold = profile.daily_appointments_threshold
        remote_appointments_threshold = profile.remote_appointments_threshold
        return {
            'dailyAppointmentsThreshold': daily_appointments_threshold, 
            'remoteAppointmentsThreshold': remote_appointments_threshold
        }