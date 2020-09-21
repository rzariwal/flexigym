from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, func

from sqlalchemy import create_engine
import pyffx

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)
    return db


def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine

encr_key = b'ab3ea3cf7bddf9a71c28f3bb42f3e24f'
mobile_chars = '01234567890'
email_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'


def detokenize_mobile(db_mobile):
    #if db_mobile == "+6594300664":
    #    return db_mobile
    #else:
        ffx = pyffx.String(encr_key, alphabet=mobile_chars, length=len(db_mobile[1:]))
        output_mobile = "+" + ffx.decrypt(db_mobile[1:])
        return output_mobile


def detokenize_email(db_email):
    db_email = db_email.split('@')
    db_email_local = db_email[0]
    db_email_domain = db_email[1]
    db_email_domain = db_email_domain.split('.')
    db_email_domain_server = db_email_domain[0]
    db_email_domain_topleveldomain = db_email_domain[1]

    ffx = pyffx.String(encr_key,
                       alphabet=email_chars,
                       length=len(db_email_local))
    output_email_local = ffx.decrypt(db_email_local)

    ffx = pyffx.String(encr_key,
                       alphabet=email_chars,
                       length=len(db_email_domain_server))
    output_email_domain_server = ffx.decrypt(db_email_domain_server)

    ffx = pyffx.String(encr_key,
                       alphabet=email_chars,
                       length=len(db_email_domain_topleveldomain))
    output_email_domain_topleveldomain = ffx.decrypt(db_email_domain_topleveldomain)

    output_email = output_email_local + "@" + output_email_domain_server + "." + output_email_domain_topleveldomain
    return output_email


def tokenize_mobile(input_mobile):
    ffx = pyffx.String(encr_key, alphabet=mobile_chars, length=len(input_mobile[1:]))
    db_mobile = "+" + ffx.encrypt(input_mobile[1:])
    return db_mobile


def tokenize_email(input_email):
    input_email = input_email.split('@')
    input_email_local = input_email[0]
    input_email_domain = input_email[1]
    input_email_domain = input_email_domain.split('.')
    input_email_domain_server = input_email_domain[0]
    input_email_domain_topleveldomain = input_email_domain[1]
    ffx = pyffx.String(encr_key,
                         alphabet=email_chars,
                         length=len(input_email_local))
    db_email_local = ffx.encrypt(input_email_local)

    ffx = pyffx.String(encr_key,
                         alphabet=email_chars,
                         length=len(input_email_domain_server))
    db_email_domain_server = ffx.encrypt(input_email_domain_server)

    ffx = pyffx.String(encr_key,
                         alphabet=email_chars,
                         length=len(input_email_domain_topleveldomain))
    db_email_domain_topleveldomain = ffx.encrypt(input_email_domain_topleveldomain)

    db_email = db_email_local + "@" + db_email_domain_server + "." + db_email_domain_topleveldomain
    return db_email


# Database Models
class SMSRequest(db.Model):
    __tablename__ = 'sms'
    request_id = Column(Integer, primary_key=True)
    requested_time = Column(DateTime(timezone=True), server_default=func.now())
    requestor_service = Column(String(50))
    requestor_service_event = Column(String(50))
    from_number = Column(String(12))
    to_number = Column(String(12))
    sms_message = Column(String(160))
    status = Column(String(20))
    message_sid = Column(String(50))
    error_message = Column(String(300))
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    def to_json(self):
        return {
            'request_id' : self.request_id,
            'requested_time': self.requested_time,
            'requestor_service': self.requestor_service,
            'requestor_service_event': self.requestor_service_event,
            'from_number': self.from_number,
            'to_number': self.to_number,
            'sms_message': self.sms_message,
            'status': self.status,
            'message_sid': self.message_sid,
            'error_message': self.error_message,
            'updated_time': self.updated_time
        }


class EmailRequest(db.Model):
    __tablename__ = 'email'
    request_id = Column(Integer, primary_key=True)
    requested_time = Column(DateTime(timezone=True), server_default=func.now())
    requestor_service = Column(String(50))
    requestor_service_event = Column(String(50))
    from_email = Column(String(30))
    to_email = Column(String(30))
    cc_email = Column(String(30))
    bcc_email = Column(String(30))
    email_subject = Column(String(100))
    email_body = Column(String(10000))
    status = Column(String(20))
    email_sid = Column(String(50))
    error_message = Column(String(300))
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    def to_json(self):
        return {
            'request_id' : self.request_id,
            'requested_time': self.requested_time,
            'requestor_service': self.requestor_service,
            'requestor_service_event': self.requestor_service_event,
            'from_email': self.from_email,
            'to_email': self.to_email,
            'cc_email': self.cc_email,
            'bcc_email': self.bcc_email,
            'email_subject': self.email_subject,
            'email_body': self.email_body,
            'status': self.status,
            'email_sid': self.email_sid,
            'error_message': self.error_message,
            'updated_time' : self.updated_time
        }

