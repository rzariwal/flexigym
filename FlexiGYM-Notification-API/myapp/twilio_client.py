from twilio.rest import Client

account_sid = 'AC9bfad63e76faf02badfa94d9a3851d77'
auth_token = '323236214caba6aa2cabb6cb87eb8316'
from_number = '+12064663506'


class TwilioClient:
    twilio_client = None

    def __init__(self):
        if TwilioClient.twilio_client is None:
            self.twilio_client = Client(account_sid, auth_token)

    def send_message(self, to, message):
        res_message = self.twilio_client.messages.create(
            to=to,
            from_=from_number,
            body=message
        )
        return res_message
