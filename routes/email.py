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
        print(thread)
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
            print("sender", sender)
            print("send", send_time)
            print("receive", receive_time)
            response_time = (receive_time - send_time).total_seconds()
            # response_times[sender].append(response_time)
            response_times[receiver].append(response_time)

            # response_time = to_working_seconds(send_time, receive_time, work_start, work_end, user_timezones[receiver])
            # response_times[receiver].append(response_time)

    average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
    return average_response_times

# Example input
# data = [{'subject': 'tKcYupNci4', 'timeSent': '2024-05-01T09:08:06+08:00', 'sender': 'QNwCT', 'receiver': 'T3zRu'}, {'subject': 'RE: tKcYupNci4', 'timeSent': '2024-05-01T16:15:41-04:00', 'sender': 'T3zRu', 'receiver': 'Tdhfq'}, {'subject': 'RE: RE: tKcYupNci4', 'timeSent': '2024-05-03T11:04:56+08:00', 'sender': 'Tdhfq', 'receiver': 'T3zRu'}, {'subject': 'RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-03T15:20:01-04:00', 'sender': 'T3zRu', 'receiver': '7cfGW'}, {'subject': 'RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-06T11:06:24-04:00', 'sender': '7cfGW', 'receiver': '4y4sP'}, {'subject': 'RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-07T13:55:11-07:00', 'sender': '4y4sP', 'receiver': '3bTKa'}, {'subject': 'RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-08T16:45:27+08:00', 'sender': '3bTKa', 'receiver': 'fIyDV'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-09T15:01:33+08:00', 'sender': 'fIyDV', 'receiver': '3bTKa'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-09T15:34:49+08:00', 'sender': '3bTKa', 'receiver': 'T3zRu'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-09T14:12:42-04:00', 'sender': 'T3zRu', 'receiver': '0s9oZ'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-10T14:30:23+02:00', 'sender': '0s9oZ', 'receiver': '7pYtF'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-10T15:52:05-04:00', 'sender': '7pYtF', 'receiver': 'z7XOj'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-13T15:55:53+02:00', 'sender': 'z7XOj', 'receiver': 'd93v6'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-14T16:43:41+10:00', 'sender': 'd93v6', 'receiver': '0ATul'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-15T14:08:04-07:00', 'sender': '0ATul', 'receiver': 'QNwCT'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-16T14:50:36+08:00', 'sender': 'QNwCT', 'receiver': '4y4sP'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-17T09:58:04-07:00', 'sender': '4y4sP', 'receiver': 'Xw4MC'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-20T11:03:38+08:00', 'sender': 'Xw4MC', 'receiver': 'd93v6'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-20T15:24:35+10:00', 'sender': 'd93v6', 'receiver': '4eMGR'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-21T13:16:38+10:00', 'sender': '4eMGR', 'receiver': 'z3CX0'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-21T12:20:04-04:00', 'sender': 'z3CX0', 'receiver': 'x3GWP'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-21T09:31:05-07:00', 'sender': 'x3GWP', 'receiver': '7pYtF'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-21T17:25:12-04:00', 'sender': '7pYtF', 'receiver': '4eMGR'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-22T12:14:16+10:00', 'sender': '4eMGR', 'receiver': 'PFWVI'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-22T10:15:34+08:00', 'sender': 'PFWVI', 'receiver': 'fIyDV'}, {'subject': 'RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: RE: tKcYupNci4', 'timeSent': '2024-05-23T10:14:28+08:00', 'sender': 'fIyDV', 'receiver': 'DvJJC'}]
    
# email = data.get
# Calculate and print the average response times
# average_response_times = calculate_response_times(data['emails'], data['users'])
# print(json.dumps(average_response_times, indent=4))
# print(json.dumps({"response": average_response_times}))