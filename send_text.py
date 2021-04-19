import os
from azure.communication.sms import SmsClient


# Create the SmsClient object which will be used to send SMS messages
sms_client = SmsClient.from_connection_string('endpoint=https://armtexttest.communication.azure.com/;accesskey=5EMxfFuvkAoVA77e1U1eG9w8SJwBKAgXID1r7fIiLWk1rEfTcxMY9wWYs/ysRFD+a3bDjz9YhrfkJ8cnCymR/g==')



def send_text(tel_number, text):
    sms_responses = sms_client.send(
    from_="+18334821558", # has to be this number, it has been purchased
    # to=["+12103820029", "+12103834324", "+19728375227"], #this is how you do multiple numbers
    to=tel_number,
    message=text
    ) # optional property


send_text('+14693867024', "This is sunday")




def send_medicine_reminder(tel_number):
    sms_responses = sms_client.send(
    from_="+18334821558", # has to be this number, it has been purchased
    # to=["+12103820029", "+12103834324", "+19728375227"], #this is how you do multiple numbers
    to=tel_number,

    message='Did you take your medicine?'
    ) # optional property


send_text('+14693867024')
