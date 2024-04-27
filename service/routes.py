import logging
from flask import request, jsonify # type: ignore
from werkzeug.exceptions import MethodNotAllowed, NotFound, InternalServerError # type: ignore
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, current_user # type: ignore
from flask_socketio import emit # type: ignore

from . import app
from . import socketio
from service.search.search_service import SearchService
from service.appointments.appointments_service import AppointmentsService
from service.configure_appointments.configure_appointments import ConfigureAppointments
from service.auth.auth_service import AuthService, InvalidCredentialsError, DuplicateCredentialsError
from service.auth.models import UserModel

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Callbacks
@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Returns the user's identity.

    Args:
        user (dict): The user object.

    Returns:
        int: The user's ID.

    """
    if user is None:
        return None
    return user['id']

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Callback function for looking up a user based on JWT data.

    Args:
        _jwt_header (dict): The JWT header.
        jwt_data (dict): The JWT data.

    Returns:
        dict or None: The user dictionary if found, None otherwise.
    """
    identity = jwt_data["sub"]
    if len(UserModel().get_users()) == 0:
        return None
    user = list(filter(lambda x: x["id"] == identity, UserModel().get_users()))[0]
    return user

# Auth
@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.

    This function receives a JSON object containing user information
    and attempts to log in the user using the AuthService.login method.
    If the login is successful, an access token is created and returned
    along with the user's ID.

    Returns:
        A JSON response containing the access token and user ID.

    Raises:
        InvalidCredentialsError: If the provided credentials are invalid.
    """
    userInfo = request.get_json()
    try:
        user = AuthService.login(userInfo)
    except InvalidCredentialsError as e:
        return jsonify({'message': e.message}), 401
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token, user=user["id"])

@app.route("/logout", methods=["POST"])
def logout_with_cookies():
    """
    Logout the user and unset the JWT cookies.

    Returns:
        Flask Response: A JSON response indicating the success of the logout operation.
    """
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# Signup
@app.route("/signup", methods=["POST"])
def signup():
    """
    Handle the signup request.

    This function receives a POST request with user information in JSON format.
    It calls the `AuthService.signUp` method to create a new user account.
    If the user already exists, a `DuplicateCredentialsError` is raised and a 409 response is returned.
    Otherwise, a successful signup message is returned.

    Returns:
        A JSON response with either an error message or a success message.
    """
    newUser: dict = request.get_json()
    try:
        AuthService.signUp(newUser)
    except DuplicateCredentialsError as e:
        return jsonify({'message': e.message}), 409
    return jsonify({'msg': 'signup successful'})

# Appointments socket
@socketio.on('appointments')
def appointments(json):
    """
    Handle the 'appointments' event from the client.

    Parameters:
    - json (list): A list containing the appointment and user_id.

    Returns:
    None
    """
    app.logger.info('request to add appointments')
    appointment = json[0]
    user_id = json[1]
    AppointmentsService.add(user_id, appointment)
    emit('appointments', [AppointmentsService.appointments(user_id), user_id], broadcast=True)

@app.route('/appointments')
@jwt_required()
def get_appointments():
    """
    Retrieves appointments for the current user.

    Returns:
        A JSON response containing the appointments for the current user.
    """
    app.logger.info('request for appointments')
    response = AppointmentsService.appointments(current_user["id"])
    print(response)
    return jsonify(response)

# Appointment fields
@app.route('/appointment-fields', methods=['PUT', 'GET'])
@jwt_required()
def appointment_fields():
    """
    Endpoint for managing appointment fields.

    PUT method:
    - Adds appointment fields for the current user.
    - Expects a JSON payload containing the appointment fields.
    - Returns the updated appointment fields for the current user.

    GET method:
    - Retrieves the appointment fields for the current user.
    - Returns the appointment fields.

    Requires authentication using JWT.

    Returns:
        JSON: The updated or retrieved appointment fields.
    """
    if request.method == 'PUT':
        app.logger.info('request to add appointments')
        fields = request.get_json()
        ConfigureAppointments().set_appointment_fields(current_user["id"], fields)
        return ConfigureAppointments().get_appointment_fields(current_user["id"])
    else:
        app.logger.info('request for appointments')
        return ConfigureAppointments().get_appointment_fields(current_user["id"])

@app.route('/search', methods=['GET'])
def search():
    """
    Endpoint for searching appointments based on a search term.

    Args:
        None

    Returns:
        A JSON response containing the search results.

    """
    search_term = request.args.get('q')
    app.logger.info('request to search appointments')
    results = SearchService.search_service(search_term)
    return jsonify(results)

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    """
    Error handler for MethodNotAllowed exception.

    Args:
        e (MethodNotAllowed): The MethodNotAllowed exception object.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code 405.
    """
    response = {
        'error': 'Method Not Allowed',
        'message': str(e)
    }
    return jsonify(response), 405

@app.errorhandler(NotFound)
def handle_not_found(e):
    """
    Error handler for handling NotFound exceptions.

    Args:
        e (NotFound): The NotFound exception object.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code 404.
    """
    response = {
        'error': 'Not Found',
        'message': str(e)
    }
    return jsonify(response), 404

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    """
    Error handler for Internal Server Error.

    Args:
        e: The exception object representing the error.

    Returns:
        A JSON response containing the error message and status code 500.
    """
    response = {
        'error': 'Internal Server Error',
        'message': str(e)
    }
    return jsonify(response), 500
