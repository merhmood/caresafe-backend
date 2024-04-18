from service.auth.models import Models_user
import uuid

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
        if(email != Models_user.get_user()[0]['email'] or password != Models_user.get_user()[0]['password']):
            raise InvalidCredentialsError('Wrong email or password')
        return Models_user.get_user()[0]
    
    def signUp(userInfo: dict):
        newUser = userInfo['signUp']
        for user in Models_user.get_user():
            if(user["email"] == newUser["email"] or user["name"] == newUser["name"]):
                raise DuplicateCredentialsError("information already exist")
        id = str(uuid.uuid4())
        Models_user.add_user({"id":id,**newUser})