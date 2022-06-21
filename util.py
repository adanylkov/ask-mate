import time
import datetime
import connection


def convert_time(timestamp, format="%d %B %Y, %H:%M"):
    _time = time.localtime(int(timestamp))
    return time.strftime(format, _time)


def make_timestamp():
    return int(time.time())


def create_id():
    id = int(connection.read_last_id("last_id.txt"))+1
    connection.write_last_id("last_id.txt", id)
    return id

def sort_by_time(question):
    submission_time = int(question["submission_time"])
    return submission_time


if __name__ == "__main__":
    print(convert_time(make_timestamp()))
    print(make_timestamp())
