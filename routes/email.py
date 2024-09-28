# import json
# from datetime import datetime, timedelta
# import pytz

# # def parse_time(time_str):
# #     return datetime.fromisoformat(time_str)

# def parse_time(time_str, timezone):
#     # Parse the time string to a naive datetime object
#     local_time = datetime.fromisoformat(time_str)
    
#     # If the datetime object is not naive, make it naive
#     if local_time.tzinfo is not None:
#         local_time = local_time.replace(tzinfo=None)
    
#     # Localize the naive datetime object to the given timezone
#     local_time = timezone.localize(local_time)
    
#     # Convert the localized time to UTC
#     return local_time.astimezone(pytz.utc)

# def calculate_response_times(emails, users):
#     user_timezones = {user['name']: pytz.timezone(user['officeHours']['timeZone']) for user in users}

# # The time elapsed between the moment Bob received the email and the time he answered is 60 hours, or 216 000 seconds
# # The time elapsed between the moment Alice received Bob's response and the time she answered is 30 hours and 5 minutes, or 108 300 seconds


#     # print(user_timezones)
#     response_times = {user['name']: [] for user in users}

#     email_threads = {}
#     # Group emails by subject
#     for email in emails:
#         subject = email['subject']
#         while subject.startswith("RE: "):
#             subject = subject[4:]
#         if subject not in email_threads:
#             email_threads[subject] = []
#             # subject key and value is list of all emails with that subject
#         email_threads[subject].append(email)

#     for thread in email_threads.values(): # thread is a list of emails with the same subject
#         thread.sort(key=lambda x: parse_time(x['timeSent'], user_timezones[x['sender']])) # 
#         print(thread)
#         for i in range(0, len(thread) - 1):
#             sender = thread[i]['sender']
#             print("sender", sender)
#             receiver = thread[i+1]['sender']
#             print("receiver", receiver)
#             send_time = parse_time(thread[i]['timeSent'], user_timezones[sender])
#             print(send_time)
#             receive_time = parse_time(thread[i+1]['timeSent'], user_timezones[receiver])
#             print(receive_time)
#             response_time = (receive_time - send_time).total_seconds()
#             print(response_time)
#             response_times[sender].append(response_time)

#     average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
#     return average_response_times

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

# # Calculate and print the average response times
# average_response_times = calculate_response_times(data['emails'], data['users'])
# print(json.dumps(average_response_times, indent=4))

import json
from datetime import datetime, timedelta, time
import pytz

def parse_time(time_str, timezone):
    local_time = datetime.fromisoformat(time_str)
    # if local_time.tzinfo is not None:
    #     local_time = local_time.replace(tzinfo=None)
    # local_time = timezone.localize(local_time)
    # return local_time.astimezone(pytz.utc)
    return local_time

def to_working_seconds(start, end, work_start, work_end, tz):
    if start.tzinfo is None:
        start = tz.localize(start)
    else:
        start = start.astimezone(tz)
    
    if end.tzinfo is None:
        end = tz.localize(end)
    else:
        end = end.astimezone(tz)
    
    if start > end:
        return 0
    
    total_seconds = 0
    current = start
    
    # print("local start", start)
    # print("local end", end)

    while current < end:
        print("while current", current)
        if current.weekday() >= 5:  # Skip weekends
            print("current", current)
            print("current.weekday()", current.weekday())
            current += timedelta(days=(7 - current.weekday()))
            current = current.replace(hour=work_start.hour, minute=work_start.minute, second=0, microsecond=0)
            print("after weekend", current)
            continue
        
        if current.time() < work_start:
            current = current.replace(hour=work_start.hour, minute=work_start.minute, second=0, microsecond=0)
            print("current", current)
        elif current.time() >= work_end:
            print("another day before", current)
            current += timedelta(days=1)
            current = current.replace(hour=work_start.hour, minute=work_start.minute, second=0, microsecond=0)
            print("another day after", current)
            continue
        
        next_end = min(end, current.replace(hour=work_end.hour, minute=work_end.minute, second=0, microsecond=0))
        extra_seconds = (next_end - current).total_seconds()
        print("extra_seconds", extra_seconds)
        total_seconds += extra_seconds
        current = next_end
        if current.time() >= work_end:
            print("another day", current)
            current += timedelta(days=1)
            current = current.replace(hour=work_start.hour, minute=work_start.minute, second=0, microsecond=0)
    
    print("total_seconds", total_seconds)
    return total_seconds

def calculate_response_times(emails, users):
    user_timezones = {user['name']: pytz.timezone(user['officeHours']['timeZone']) for user in users}
    user_work_hours = {user['name']: (time(user['officeHours']['start']), time(user['officeHours']['end'])) for user in users}

    response_times = {user['name']: [] for user in users}

    email_threads = {}
    for email in emails:
        subject = email['subject']
        while subject.startswith("RE: "):
            subject = subject[4:]
        if subject not in email_threads:
            email_threads[subject] = []
        email_threads[subject].append(email)

    for thread in email_threads.values():
        thread.sort(key=lambda x: parse_time(x['timeSent'], user_timezones[x['sender']]))
        for i in range(0, len(thread) - 1):
            sender = thread[i]['sender']
            receiver = thread[i+1]['sender']
            send_time = parse_time(thread[i]['timeSent'], user_timezones[sender])
            receive_time = parse_time(thread[i+1]['timeSent'], user_timezones[receiver])
            work_start, work_end = user_work_hours[receiver]
            # print("send", send_time)
            # print("receive", receive_time)
            # print(response_time)

            # directly minus response time
            # response_time = (receive_time - send_time).total_seconds()
            # response_times[sender].append(response_time)

            response_time = to_working_seconds(send_time, receive_time, work_start, work_end, user_timezones[receiver])
            response_times[receiver].append(response_time)

    average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
    return average_response_times

# Example input
data = {
        "emails": [
            {
                "subject": "JXXOa19SUO",
                "timeSent": "2024-05-01T11:33:37+02:00",
                "sender": "3mCSR",
                "receiver": "rPKRL"
            },
            {
                "subject": "RE: JXXOa19SUO",
                "timeSent": "2024-05-02T16:28:00+08:00",
                "sender": "rPKRL",
                "receiver": "3mCSR"
            }
        ],
        "users": [
            {
                "name": "rPKRL",
                "officeHours": {
                    "timeZone": "Hongkong",
                    "start": 8,
                    "end": 17
                }
            },
            {
                "name": "3mCSR",
                "officeHours": {
                    "timeZone": "Europe/Paris",
                    "start": 9,
                    "end": 18
                }
            }
        ]
    }
# Calculate and print the average response times
average_response_times = calculate_response_times(data['emails'], data['users'])
# print(json.dumps(average_response_times, indent=4))
print(json.dumps({"response": average_response_times}))