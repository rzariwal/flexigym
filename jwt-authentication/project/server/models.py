# project/server/models.py

import datetime
import jwt
import pyffx

from project.server import app, db, bcrypt


encr_key=b'ab3ea3cf7bddf9a71c28f3bb42f3e24f'
mobile_chars='01234567890'
email_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-'

class Tokenize:
    @staticmethod
    def tokenize_mobile(input_mobile):
        ffx = pyffx.String(encr_key, alphabet=mobile_chars, length=len(input_mobile[1:]))
        db_mobile = "+" + ffx.encrypt(input_mobile[1:])
        return db_mobile

    @staticmethod
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

    @staticmethod
    def detokenize_mobile(db_mobile):
        ffx = pyffx.String(encr_key, alphabet=mobile_chars, length=len(db_mobile[1:]))
        output_mobile = "+" + ffx.decrypt(db_mobile[1:])
        return output_mobile

    @staticmethod
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

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    mobile = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password, mobile, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.mobile = mobile

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


