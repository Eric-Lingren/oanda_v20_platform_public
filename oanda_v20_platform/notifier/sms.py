from twilio.rest import Client


class TwilioSMS:
    def __init__(self, twilio_sid, twilio_token, twilio_number, recipient_number):
        self.account_sid = twilio_sid
        self.auth_token = twilio_token
        self.twilio_number = twilio_number 
        self.recipient_number = recipient_number
        
    def send_text(self, msg):
        client = Client(self.account_sid, self.auth_token) 
        client.messages.create( from_=self.twilio_number ,  to=self.recipient_number, body=msg ) 