from flask import request, jsonify
from werkzeug.exceptions import MethodNotAllowed, NotFound, InternalServerError
from . import app
from service.appointment.appointments_service import AppointmentsService

# Appointments
@app.route('/appointments', methods=['POST', 'PUT', 'GET'])
def appointments():
    '''
        handles the request for adding, configuring and requesting
        for appointments
    '''
    if (request.method == 'POST'):
        app.logger.info('request to add appointments')
        appointment = request.get_json()
        return AppointmentsService.add(appointment)
    
    if (request.method == 'PUT'):
        app.logger.info('request to configure appointments')
        fields = request.get_json()
        return AppointmentsService.configure(fields)
    
    if (request.method == 'GET'):
        app.logger.info('request for appointments')
        return AppointmentsService.appointments()

# Custom error handler for 405 Method Not Allowed
@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    response = {
        "error": "Method Not Allowed",
        "message": str(e)
    }
    return jsonify(response), 405

# Custom error handler for 404 Method Not Found
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = {
        "error": "Not Found",
        "message": str(e)
    }
    return jsonify(response), 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    response = {
        "error": "Internal Server Error",
        "message": str(e)
    }
    return jsonify(response), 500