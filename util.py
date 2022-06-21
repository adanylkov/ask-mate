import time


def convert_time(timestamp, format="%d %B %Y, %H:%M"):
    _time = time.localtime(int(timestamp))
    return time.strftime(format, _time)


def make_timestamp():
    pass


if __name__ == "__main__":
    print(convert_time(1493368154))
