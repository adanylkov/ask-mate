import time
import connection
import datetime


def convert_time(timestamp, format="%d %B %Y, %H:%M"):
    _time = time.localtime(int(timestamp))
    return time.strftime(format, _time)


def make_timestamp():
    datetime.datetime.now()


def question_datetime_to_epoch(question):
    datetime = question.get('submission_time')
    question['submission_time'] = int(datetime.timestamp()) if datetime else 0
    return question


def create_id(is_question=True):
    id = connection.read_last_id("last_id.txt")
    question_id, answer_id = id.split(',')
    if is_question:
        question_id = int(question_id) + 1
    else:
        answer_id = int(answer_id) + 1
    connection.write_last_id("last_id.txt", f"{question_id},{answer_id}")
    return question_id if is_question else answer_id


def sort_by(question, order):
    sort_by = {
            'title': (str,'title'),
            'submission_time': (int, 'submission_time'),
            'message': (str,'message'),
            'number_of_views': (int, 'view_number'),
            'number_of_votes': (int, 'vote_number'),
            }

    func, key = sort_by[order]
    return func(str(question[key]).lower())


if __name__ == "__main__":
    import data_manager
    question = data_manager.get_question_by_id(1)
    ret = sort_by(question, "number_of_views")
    print(f'{ret=}')
    print(f'{type(ret)=}')
