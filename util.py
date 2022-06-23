import connection
from datetime import datetime
import time

def get_current_time():
    timestamp = int(time.mktime(datetime.now().timetuple()))
    return timestamp
def get_date_format(data):
    for row in data:
        timestamp = int(row["submission_time"])
        row["submission_time"] = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
    return data

def create_fields(title, question, image_path):
    question_dictionary = {'id': generate_new_id('last_id.txt'),
                           'submission_time': get_current_time(),
                           'view_number': 0,
                           'vote_number': 0,
                           'title': title,
                           'message': question,
                           'image': image_path}
    return question_dictionary

def generate_new_id(filename):
    with open(filename, 'r') as file:
        last_id = int(file.read())
    with open(filename, 'w') as file:
        file.write(str(last_id + 1))
    return last_id + 1