import argparse
import os
from twilio.rest import Client
import datetime
import dropbox
import requests
from nlt_birthday_accessor import query_db
import sqlite3
import time
from secrets import TWI_ACCOUNT_SID, TWI_AUTH_TOKEN, DROPB_AUTH_TOKEN, TWI_PHONE_NUMBER
import random
from manage_contacts import query_contact_numbers


def main():
    message_body = args.directmessage
    messages = ['Happy Birthday to our very own {}.  We are especially grateful for you.  Thank you for being a tremendous blessing to our NLT church family.',
              'Birthday Blessings to our very own {}.  You are loved and appreciated by your New Life Tabernacle church family.  Have a blessed day.',
              'Congratulations and Happy Birthday to our very own {}.  May God continue to bless you for your love and sacrifice for the advancement of New Life Tabernacle\'s ministry.']

    today = datetime.date.today()
    today_mmdd = int('{}{}'.format(today.month, "{0:0>2}".format(today.day)))

    conn = sqlite3.connect('newlifetabernacle_members.db')

    birthday_list = query_db(conn, today_mmdd)
    contact_list = query_contact_numbers(conn)
    
    dbx = dropbox.Dropbox(DROPB_AUTH_TOKEN)
    
    client = Client(TWI_ACCOUNT_SID, TWI_AUTH_TOKEN)


    for i in birthday_list:
        if i[0] in ['Barbara Parrish', 'Shirley Lewis-Thomas', 'Wynette Vaughn']:
            proper_name = f'Mother {i[0]}'
        elif i[0] in ['Eric Figueroa Sr.', 'David J. Billings III']:
            proper_name = f'Archbishop {i[0]}'
        elif i[0] in ['Robert Thomas', 'Robert Butler']:
            proper_name = f'Bishop {i[0]}'
        else:
            proper_name = i[0]

        if not message_body:
            message_body = random.choice(messages).format(proper_name)   
           
        
        for contact in contact_list: 
                       
            client.messages.create(
            body= message_body,
            from_ = TWI_PHONE_NUMBER,
            media_url= [f"{i[3]}"],
            to= f"+{contact}")
        time.sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Enter override birthday message")
    parser.add_argument("-d", "--directmessage", type=str, help="Enter a default message")
    args = parser.parse_args()

    main()