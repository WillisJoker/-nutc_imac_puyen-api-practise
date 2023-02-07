import random
import uuid


def getRandom():
    result = str(random.randint(1000, 9999))
    return result

def uuid_6():
    return str(uuid.uuid4())[:6]

def utc_time(data):
    split_time = data.split(" ")
    split_time.insert(1, 'T')
    split_time.insert(3, '+08:00')
    final_string = ''.join(split_time)
    return final_string


