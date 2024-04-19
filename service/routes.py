from flask import request, jsonify # type: ignore
from werkzeug.exceptions import MethodNotAllowed, NotFound, InternalServerError # type: ignore
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, current_user # type: ignore

from . import app
from service.appointments.appointments_service import AppointmentsService
from service.appointment_fields.appointment_fields_service import AppointmentFields
from service.auth.auth_service import AuthService, InvalidCredentialsError, DuplicateCredentialsError
from service.auth.models import UserModel

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

# JWT Callbacks
@jwt.user_identity_loader
def user_identity_lookup(user):
    '''
        Register a callback function that takes whatever object is passed in as the
        identity when creating JWTs and converts it to a JSON serializable format.
    '''
    if(user == None):
        return None
    return user['id']

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    '''
        Register a callback function that loads a user from your database whenever
        a protected route is accessed. This should return any python object on a
        successful lookup, or None if the lookup failed for any reason (for example
        if the user has been deleted from the database).
    '''
    identity = jwt_data["sub"]
    if(len(UserModel().get_users()) == 0):
        return None
    user = list(filter(lambda x: x["id"] == identity, UserModel().get_users()))[0]
    return user

# Auth
@app.route('/login', methods=['POST'])
def login():
    '''
        Create a route to authenticate your users and return JWTs. The
        create_access_token() function is used to actually generate the JWT.
    '''
    userInfo = request.get_json()
    print(userInfo)
    global user
    try:
        
        user = AuthService.login(userInfo)
    except InvalidCredentialsError as e:
        return jsonify({'message':e.message}), 401
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)

@app.route("/logout", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# Signup
@app.route("/signup", methods=["POST"])
def signup():
    '''
        Create a route to register your users and return JWTs. 
        The create_access_token()
    '''
    newUser: dict = request.get_json()
    print(newUser)
    try: 
        AuthService.signUp(newUser)
    except DuplicateCredentialsError as e:
        return jsonify({'message':e.message}), 409
    return jsonify({'msg': 'signup succesful'})

# Appointments
@app.route('/appointments', methods=['POST', 'GET'])
@jwt_required()
def appointments():
    '''
        Handles the request for adding and retrieving appointments
        for appointments
    '''
    if (request.method == 'POST'):
        app.logger.info('request to add appointments')
        appointment = request.get_json()
        return AppointmentsService.add(current_user["id"], appointment)
    else:
        app.logger.info('request for appointments')
        return AppointmentsService.appointments(current_user["id"])

# Appointment fields
@app.route('/appointment-fields', methods=['PUT', 'GET'])
@jwt_required()
def appointment_fields():
    '''
        Handles the request for configuring and retrieving of appointment fields
    '''
    print(current_user["id"])
    if (request.method == 'PUT'):
        app.logger.info('request to add appointments')
        fields = request.get_json()
        print(fields)
        AppointmentFields().set_appointment_fields(current_user["id"], fields)
        return  AppointmentFields().get_appointment_fields(current_user["id"])
    else:
        print("ran")
        app.logger.info('request for appointments')
        return AppointmentFields().get_appointment_fields(current_user["id"])
    

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    '''
        Custom error handler for 405 Method Not Allowed
    '''
    response = {
        'error': 'Method Not Allowed',
        'message': str(e)
    }
    return jsonify(response), 405

@app.errorhandler(NotFound)
def handle_not_found(e):
    '''
        Custom error handler for 404 Method Not Found
    '''
    response = {
        'error': 'Not Found',
        'message': str(e)
    }
    return jsonify(response), 404

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    '''
        Custom error handler for 500 Internal Server Error
    '''
    response = {
        'error': 'Internal Server Error',
        'message': str(e)
    }
    return jsonify(response), 500