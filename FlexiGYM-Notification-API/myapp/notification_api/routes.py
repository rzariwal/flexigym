from flask import json, jsonify, request
from . import notification_api_blueprint
from models import db, SMSRequest, EmailRequest
import logging
from twilio_client import TwilioClient, from_number
from gmail_client import GmailClient, sender_email
import requests
from smtplib import SMTPException

ADVERTISE_API_OK = True
# ADVERTISE_URL = "http://35.198.220.113:9100/packagesApi"
ADVERTISE_URL = "http://flexigym-advertise-service2:9100/packagesApi/"

NOTIFICATION_API_OK = True
# NOTIFICATION_URL = "http://35.198.220.113:7000/api/sms/send_sms"
NOTIFICATION_URL = "http://flexigym-notification-api:7000/api/sms/send_sms"

SUBSCRIBE_API_OK = True
# NOTIFICATION_URL = "http://35.198.220.113:7000/api/sms/send_sms"
SUBSCRIBE_URL = "http://flexigym-subscribe-api:6200/"


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
    return jsonify(message_sid=message_sid, message_status=message_status,
                   error_message=error_message), http_status_code


@notification_api_blueprint.route('/api/sms/list_sms/<string:to_number>', methods=['GET'])
def list_sms(to_number: str):
    # to_number = request.json['to_number']

    record = SMSRequest.query.filter_by(to_number=to_number).first()

    if record:
        records = []
        for record in SMSRequest.query.filter_by(to_number=to_number).all():
            records.append(record.to_json())

        response = jsonify({
            'results': records
        })

        return response, 200
    else:
        return jsonify(message='Application has not sent any SMS to the given Phone number'), 404


@notification_api_blueprint.route('/api/email/send_email', methods=['POST'])
def send_email():
    to_email = request.json['to_email']
    email_subject = request.json['email_subject']
    email_content = request.json['email_content']

    email_text = 'Subject: {}\n\n{}'.format(email_subject, email_content)
    http_status_code = 200
    error_message = None

    try:
        gmail_client = GmailClient()
        gmail_client.send_email(to_email, email_text)

    except SMTPException as exception:
        http_status_code = 400
        error_message = str(exception.args[0])
        pass
    finally:
        if http_status_code == 200:
            message = "Email Sent."
        else:
            message = "Error in Sending Email."

        email_message_model_object = EmailRequest(to_email=to_email,
                                                  from_email=sender_email,
                                                  email_body=email_content,
                                                  email_subject=email_subject,
                                                  status=message,
                                                  error_message=error_message)

        db.session.add(email_message_model_object)
        db.session.commit()
        # logging.info('SID: {}, Status: {}'.format(message_sid, message_status))

    return jsonify(message=message), http_status_code


@notification_api_blueprint.route('/api/email/list_email/<string:email>', methods=['GET'])
def list_email(email: str):
    record = EmailRequest.query.filter_by(to_email=email).first()

    if record:
        records = []
        for record in EmailRequest.query.filter_by(to_email=email).all():
            records.append(record.to_json())

        response = jsonify({
            'results': records
        })

        return response, 200
    else:
        return jsonify(message='Application has not sent any Email to the given Email Id.'), 404


@notification_api_blueprint.route('/testProductList', methods=['GET', 'POST'])
def testProductList():
    ADVERTISE_API_OK = True
    # ADVERTISE_URL = "http://35.198.220.113:9100/packagesApi"
    ADVERTISE_URL = "http://flexigym-advertise-service2:9100/packagesApi/"
    if ADVERTISE_API_OK:
        response = requests.get(url=ADVERTISE_URL + "/" + str(1))
        return jsonify(message=response.json()['packages']["package_name"])


@notification_api_blueprint.route('/testCheckout', methods=['GET', 'POST'])
def testCheckout():
   response = None
   try:
        cart = {"cart_id": "1"}
        if SUBSCRIBE_API_OK:
            response = requests.post(url=SUBSCRIBE_URL + "checkout", json=cart)
        if response.status_code == 200:
            return jsonify(message=response.json)
   except Exception as e:
       print(e)
       return jsonify(message=response.json)