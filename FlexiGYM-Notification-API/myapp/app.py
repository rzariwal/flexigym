"""
from flask import Flask, jsonify, request, json
from twilio.rest import Client
import logging
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.models import *


app = Flask(__name__)
# Since we will use SQL Alchemy we need to specify the file which will be used as database.
basedir = os.path.abspath(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir + 'flexigym-notification_api.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
# app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 # we need to initialize our database before we actually start using it
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

# Create and configure logger
logging.basicConfig(filename="../app.log",
                    format='%(asctime)s-%(name)s-%(filename)s:%(lineno)s-%(funcName)s()-%(levelname)s - %(message)s',
                    filemode='w')
# Creating an log object
logger = logging.getLogger()

# Set the threshold of logger
logger.setLevel(level=logging.INFO)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("DB Created!")
# Should goto IDE's Terminal and run command 'flask db_create'  to run this function.


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("DB Dropped!")
# Should goto IDE's Terminal and run command 'flask db_drop'  to run this function.


@app.cli.command('db_seed')
def db_seed():
    # Should goto IDE's Terminal and run command 'flask db_seed'  to run this function.
    test_user = User(first_name='William',
                     last_name='Herschel',
                     email='test@domain.com',
                     password='P@ssw0rd')

    db.session.add(test_user)
    db.session.commit()
    print('DB has been Seeded!')

# Authenticate the Client
# twilio_client = Client(account_sid, auth_token)



# classes for marshmallow
class SMSRequestSchema(ma.Schema):
    class Meta:
        fields = ('request_id', 'requested_time', 'requestor_service', 'requestor_service_event', 'from_number', 'to_number', 'sms_message', 'status', 'message_sid', 'updated_time')


class EmailRequestSchema(ma.Schema):
    class Meta:
        fields = ('request_id', 'requested_time', 'requestor_service', 'requestor_service_event', 'from_email', 'to_email', 'cc_email', 'bcc_email', 'email_subject', 'email_body', 'status', 'email_sid', 'updated_time')


sms_request_schema = SMSRequestSchema()
email_request_schemas = SMSRequestSchema(many=True)  # To serialize multiple user objects

email_request_schema = EmailRequestSchema()
email_request_schemas = EmailRequestSchema(many=True)
"""

# from project setup reference
import setup
app = setup.create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
