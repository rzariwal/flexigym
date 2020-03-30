from flask import json, jsonify, request
from . import notification_api_blueprint
from models import db, SMSRequest
import logging
from twilio_client import TwilioClient, from_number


@notification_api_blueprint.route("/api/sms/docs.json", methods=['GET'])
def swagger_api_docs_yml():
    with open('swagger.json') as fd:
        json_data = json.load(fd)

    return jsonify(json_data)


@notification_api_blueprint.route('/api/sms/send_sms', methods=['POST'])
def send_sms():
    to_number = request.json['to_number']
    content = request.json['content']

    twilio_client = TwilioClient()
    message_sid = None
    message_status = "error"
    try:
        message = twilio_client.send_message(to=to_number, message=content)
        message_sid = message.sid
        message_status = message.status
        error_message = message.error_message if message.error_message else ""
        http_status_code = 200

    except Exception as exception:
        message_sid = "error"
        message_status = "error"
        error_message = exception.args[2]
        http_status_code = 400
        pass
    finally:
        sms_message_model_object = SMSRequest(from_number=from_number,
                                          to_number=to_number,
                                          sms_message=content,
                                          status=message_status,
                                          message_sid=message_sid,
                                          requestor_service="test",
                                          requestor_service_event="test-event",
                                          error_message=error_message)

        db.session.add(sms_message_model_object)
        db.session.commit()
        logging.info('SID: {}, Status: {}'.format(message_sid, message_status))
    return jsonify(message_sid=message_sid, message_status=message_status, error_message=error_message), http_status_code


@notification_api_blueprint.route('/api/sms/list_sms', methods=['POST'])
def list_sms():
    to_number = request.json['to_number']

    record = SMSRequest.query.filter_by(to_number=to_number).first()

    if record:
        records = []
        for record in SMSRequest.query.filter_by(to_number=to_number).all():
            records.append(record.to_json())

        response = jsonify({
            'results' : records
        })

        return response, 200
    else:
        return jsonify(message='Application has not sent any SMS to the given Phone number'), 404

"""
@notification_api_blueprint.route('/api/sms/sms_status', methods=['GET'])
def sms_status():
    message = twilio_client.messages(sid="SM9c764c2ec22f44e9a2a8e1dbc7472d75").fetch()

    message_sid = message.sid
    message_status = message.status

    logging.info('SID: {}, Status: {}'.format(message_sid, message_status))
    return jsonify(message_sid=message_sid, message_status=message_status)
"""

