import uuid
from service.auth.models import UserModel
from service.appointments.models import AppointmentsModel

class InvalidCredentialsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DuplicateCredentialsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AuthService():
    def login(userInfo: dict):
        email = userInfo['login']['email']
        password = userInfo['login']['password']
        users = UserModel().get_users()
        if(len(users) == 0):
            # No user found
            raise InvalidCredentialsError('No user found')
        if(len(users) > 0):
            # Check if user exists
            user = list(filter(lambda x: x["email"] == email and x["password"] == password, users))
            # If user exists, return user
            if(len(user) > 0):
                return user[0]
            # If user does not exist, raise error
            else:
                raise InvalidCredentialsError('Wrong email or password')
                
    
    def signUp(userInfo: dict):
        newUser:dict = userInfo['signUp']
        # Check if user already exists
        for user in UserModel().get_users():
            if(user["email"] == newUser["email"] or user["name"] == newUser["name"]):
                # If user exists, raise error
                raise DuplicateCredentialsError("information already exist")
        id = str(uuid.uuid4())
        # Creates default appointment fields for new user
        defaultAppointmentFields = {
            "userId": id,
            "name": "",
            "address": "",
        
        }
        # Removes confirmPassword field from newUser
        newUser.pop("confirmPassword")
        newUser["id"] = id
        UserModel().add_user(newUser)
        AppointmentsModel().configure_appointment(id, defaultAppointmentFields)