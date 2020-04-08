import smtplib
import ssl

port = 465  # For SSL
password = "Apr-2020"
sender_email = "FlexiGYM.Email@gmail.com"


class GmailClient:
    gmail_client = None
    sender_email = sender_email
    to_email = None
    email_text = None

    def __init__(self):
        if GmailClient.gmail_client is None:
            self.gmail_client = smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context())

            self.gmail_client.login(sender_email, password)


    def send_email(self, to_email, email_text):
        self.gmail_client.sendmail(sender_email, to_email, email_text)

        #self.gmail_client.quit()

