from werkzeug.security import generate_password_hash, check_password_hash
from service.routes import db
from service.auth.models import User
from service.configure_appointments.configure_appointments_service import ConfigureAppointmentsService

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
        # Extract email and password from userInfo
        email = userInfo['login']['email']
        password = userInfo['login']['password']
        
       # Query the database for the user with the specified email
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            # No user found
            raise InvalidCredentialsError('No user found')
        
        # Check if the password is correct
        if not check_password_hash(user.password, password):
            # Invalid password
            raise InvalidCredentialsError('Invalid password')
        
        # User found and password is correct
        return user
    
    def signUp(userInfo: dict):
        newUser:dict = userInfo['signUp']
        
               # Check if user already exists
        existing_user = User.query.filter((User.email == newUser["email"]) | (User.name == newUser["name"])).first()
        if existing_user is not None:
            # If user exists, raise error
            raise DuplicateCredentialsError("information already exist")

        # Hash the password
        hashed_password = generate_password_hash(newUser['password'], method='pbkdf2:sha256')

        # Create a new User object and add it to the database
        new_user = User(name=newUser['name'], state=newUser['state'], address=newUser['address'], email=newUser['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        ConfigureAppointmentsService().set_appointment_fields(new_user.id, ["name", "address"])

        # User created successfully
        return 'User created successfully'