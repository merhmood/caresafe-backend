import uuid
from service.auth.models import UserModel

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
        if(len(users) > 0):
            user = list(filter(lambda x: x["email"] == email and x["password"] == password, users))
            if(len(user) > 0):
                return user[0]
            else:
                raise InvalidCredentialsError('Wrong email or password')
                
    
    def signUp(userInfo: dict):
        newUser = userInfo['signUp']
        for user in UserModel().get_users():
            if(user["email"] == newUser["email"] or user["name"] == newUser["name"]):
                raise DuplicateCredentialsError("information already exist")
        id = str(uuid.uuid4())
        UserModel().add_user({"id":id,**newUser})