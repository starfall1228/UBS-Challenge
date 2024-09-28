import json
from datetime import datetime, timedelta
import pytz

def parse_time(time_str):
    return datetime.fromisoformat(time_str)

def calculate_response_times(emails, users):
    user_timezones = {user['name']: pytz.timezone(user['officeHours']['timeZone']) for user in users}
    response_times = {user['name']: [] for user in users}

    email_threads = {}
    for email in emails:
        subject = email['subject']
        if subject.startswith("RE:"):
            subject = subject[4:]
        if subject not in email_threads:
            email_threads[subject] = []
        email_threads[subject].append(email)

    for thread in email_threads.values():
        thread.sort(key=lambda x: parse_time(x['timeSent']))
        for i in range(1, len(thread)):
            sender = thread[i]['sender']
            receiver = thread[i-1]['receiver']
            send_time = parse_time(thread[i]['timeSent'])
            receive_time = parse_time(thread[i-1]['timeSent'])
            response_time = (send_time - receive_time).total_seconds()
            response_times[sender].append(response_time)

    average_response_times = {user: round(sum(times) / len(times)) if times else 0 for user, times in response_times.items()}
    return average_response_times

# Example input
data = {
    "emails": [
        {
            "subject": "subject",
            "sender": "Alice",
            "receiver": "Bob",
            "timeSent": "2024-01-12T15:00:00+01:00"
        },
        {
            "subject": "RE: subject",
            "sender": "Bob",
            "receiver": "Alice",
            "timeSent": "2024-01-15T09:00:00+08:00"
        },
        {
            "subject": "RE: RE: subject",
            "sender": "Alice",
            "receiver": "Bob",
            "timeSent": "2024-01-16T09:05:00+01:00"
        }
    ],
    "users": [
        {
            "name": "Alice",
            "officeHours": {
                "timeZone": "Europe/Paris",
                "start": 9,
                "end": 18
            }
        },
        {
            "name": "Bob",
            "officeHours": {
                "timeZone": "Asia/Singapore",
                "start": 8,
                "end": 17
            }
        }
    ]
}

# Calculate and print the average response times
average_response_times = calculate_response_times(data['emails'], data['users'])
print(json.dumps(average_response_times, indent=4))
