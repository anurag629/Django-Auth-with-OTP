import os
from twilio.rest import Client

account_sid = 'your twilio sid'
auth_token = 'your auth token'
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages.create(
        body=f'Hi there your verification code is - {user_code}',
        from_='your twilio number',
        to=f'+91{phone_number}'
    )
    print(message.sid)
