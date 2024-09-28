import json
from datetime import datetime, timedelta
import pytz

import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

# def parse_time(time_str):
#     return datetime.fromisoformat(time_str)

def parse_time(time_str, timezone):
    # Parse the time string to a naive datetime object
    local_time = datetime.fromisoformat(time_str)
    
    # If the datetime object is not naive, make it naive
    if local_time.tzinfo is not None:
        local_time = local_time.replace(tzinfo=None)
    
    # Localize the naive datetime object to the given timezone
    local_time = timezone.localize(local_time)
    
    # Convert the localized time to UTC
    return local_time.astimezone(pytz.utc)

def calculate_response_times(emails, users):
    user_timezones = {user['name']: pytz.timezone(user['officeHours']['timeZone']) for user in users}

# The time elapsed between the moment Bob received the email and the time he answered is 60 hours, or 216 000 seconds
# The time elapsed between the moment Alice received Bob's response and the time she answered is 30 hours and 5 minutes, or 108 300 seconds


    # print(user_timezones)
    response_times = {user['name']: [] for user in users}

    email_threads = {}
    # Group emails by subject
    for email in emails:
        subject = email['subject']
        while subject.startswith("RE: "):
            subject = subject[4:]
        if subject not in email_threads:
            email_threads[subject] = []
            # subject key and value is list of all emails with that subject
        email_threads[subject].append(email)

    for thread in email_threads.values(): # thread is a list of emails with the same subject
        thread.sort(key=lambda x: parse_time(x['timeSent'], user_timezones[x['sender']])) # 
        print(thread)
        for i in range(0, len(thread) - 1):
            sender = thread[i]['sender']
            # print("sender", sender)
            receiver = thread[i+1]['sender']
            # print("receiver", receiver)
            send_time = parse_time(thread[i]['timeSent'], user_timezones[sender])
            # print(send_time)
            receive_time = parse_time(thread[i+1]['timeSent'], user_timezones[receiver])
            # print(receive_time)
            response_time = (receive_time - send_time).total_seconds()
            # print(response_time)
            response_times[sender].append(response_time)

    average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
    return average_response_times

# # Example input
# data = {
#     "emails": [
#         {
#             "subject": "subject",
#             "sender": "Alice",
#             "receiver": "Bob",
#             "timeSent": "2024-01-12T15:00:00+01:00"
#         },
#         {
#             "subject": "RE: subject",
#             "sender": "Bob",
#             "receiver": "Alice",
#             "timeSent": "2024-01-15T09:00:00+08:00"
#         },
#         {
#             "subject": "RE: RE: subject",
#             "sender": "Alice",
#             "receiver": "Bob",
#             "timeSent": "2024-01-16T09:05:00+01:00"
#         }
#     ],
#     "users": [
#         {
#             "name": "Alice",
#             "officeHours": {
#                 "timeZone": "Europe/Paris",
#                 "start": 9,
#                 "end": 18
#             }
#         },
#         {
#             "name": "Bob",
#             "officeHours": {
#                 "timeZone": "Asia/Singapore",
#                 "start": 8,
#                 "end": 17
#             }
#         }
#     ]
# }



@app.route('/mailtime', methods=['POST'])
def mailtime():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    average_response_times = calculate_response_times(data['emails'], data['users'])
    result = average_response_times
    logging.info("My result :{}".format(result))
    return json.dumps(result)

# Calculate and print the average response times
average_response_times = calculate_response_times(data['emails'], data['users'])
print(json.dumps(average_response_times, indent=4))
