import connection
import util
import os
import database_common

def get_image_by_id(question_id, answer_id = None):
    images = os.listdir(os.path.join(os.curdir, 'static','images'))
    image_name = f"{question_id}_{answer_id if answer_id else ''}"
    for image in images:
        if image_name in image:
            return image

def delete_image(question):
    image_folder = os.path.join(os.curdir, 'static')
    image_name = question.get('image')
    image_file = os.path.join(image_folder, image_name)
    if os.path.isfile(image_file):
        os.remove(image_file)


@database_common.connection_handler
def get_question_by_id(cursor, id):
    # questions = connection.read_data_from_file('question.csv')
    # return list(filter(lambda question: question['id'] == str(id), questions)).pop()
    query = f"SELECT *\
         FROM question\
         WHERE id='{id}'"
    cursor.execute(query)
    return cursor.fetchall()

def get_answer_by_id(id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['id'] == str(id), answers)).pop()

def answers_by_question_id(question_id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['question_id'] == str(question_id), answers))


@database_common.connection_handler
def questions(cursor):
    query = """
        SELECT *
        FROM question
        """
    cursor.execute(query)
    questions = cursor.fetchall()
    return list(map(util.question_datetime_to_epoch, questions))
#
#     questions = connection.read_data_from_file('question.csv')
#     return questions

def answers():
    answers = connection.read_data_from_file('answer.csv')
    return answers


@database_common.connection_handler
def add_question(cursor, title, message, submission_time = None, view_number = None, vote_number = None, image = None):
    question = {
            "submission_time": util.make_timestamp(), #if not submission_time else submission_time,
            "view_number": 0 if not view_number else view_number,
            "vote_number": 0 if not vote_number else vote_number,
            "title": title,
            "message": message,
            "image": None if not image else image
            }
    #connection.add_data_to_file("question.csv", question, connection.QUESTION_HEADER)
    cursor.execute("""INSERT INTO question
            (submission_time, view_number, vote_number, title, message, image)
            VALUES (%(s_t)s, %(v_n)s, %(v_r)s, %(t_l)s, %(m_g)s, %(i_g)s)""",
                   {'s_t': question['submission_time'],
                    'v_n': question['view_number'],
                    'v_r': question['vote_number'],
                    't_l': question['title'],
                    'm_g': question['message'],
                    'i_g': question['image']
                    })
    query = f"SELECT id\
        FROM question\
        WHERE title LIKE '%{title}'"
    cursor.execute(query)
    return cursor.fetchall()
    #return question["id"]


def add_answer(message, question_id, submission_time = None, vote_number = None, image = None, index = 0, id = None):
    if id == None:
        id = util.create_id()
    all_answers = answers()
    answer = {
            "id": util.create_id(is_question=False) if not id else id,
            "submission_time": util.make_timestamp(),
            "vote_number": 0,
            "question_id": question_id,
            "id": id, 
            "submission_time": util.make_timestamp() if not submission_time else submission_time, 
            "vote_number": 0 if not vote_number else vote_number, 
            "message": message, 
            "image": None if not image else image}
    all_answers.insert(index, answer)
    connection.write_data_to_file('answer.csv', data=all_answers, data_header=connection.ANSWER_HEADER)


def del_question(question, edit : bool):
    all_answers = answers()
    all_questions = questions()
    question_id = question['id']
    if not edit:
        delete_image(question)
    for dicts in all_questions:
        if dicts["id"] == str(question_id):
            all_questions.pop(all_questions.index(dicts))
    connection.write_data_to_file("question.csv", all_questions, data_header=connection.QUESTION_HEADER)
    if not edit:
        for dicts in all_answers:
            if dicts["question_id"] == str(question_id):
                    delete_image(dicts)
                    all_answers.pop(all_answers.index(dicts))
        connection.write_data_to_file("answer.csv", all_answers, data_header=connection.ANSWER_HEADER)


def del_answer(answer_id, edit=False):
    all_answers = answers()
    for dicts in all_answers:
        if dicts["id"] == str(answer_id):
            if not edit:
                delete_image(dicts)
            index = all_answers.index(dicts)
            all_answers.pop(index)
            question_id = dicts["question_id"]
            connection.write_data_to_file("answer.csv", all_answers, data_header=connection.ANSWER_HEADER)
            return question_id, index


def edit_answers_question_id(question_id, new_id):
    all_answers = connection.read_data_from_file('answer.csv')
    for answer in all_answers:
        if answer['question_id'] == str(question_id):
            answer['question_id'] = str(new_id)
    connection.write_data_to_file('answer.csv', data=all_answers, data_header=connection.ANSWER_HEADER)


def edit_question(question):
    del_question(question, edit=True)
    edit_answers_question_id(question_id=question['id'], new_id=question['new_id'])
    add_question(
            title=question['title'],
            id=question['new_id'],
            submission_time=question['submission_time'],
            message=question['message'],
            view_number=question['view_number'],
            vote_number=question['vote_number'],
            image=question['image']
            )


def edit_answer(answer):
    delete_question = del_answer(answer['id'], edit=True)
    if delete_question:
        index = delete_question[1]
        add_answer(
            id = answer['id'],
            index = index,
            question_id=answer['question_id'],
            submission_time=answer['submission_time'],
            message=answer['message'],
            vote_number=answer['vote_number'],
            image=answer['image']
            )
        return answer['question_id']

def vote_up(vote_number):
    if(vote_number):
        vote_number +=1
    else:
        vote_number = 1
    return vote_number
    
def vote_down(vote_number):  
    if(vote_number):
        vote_number -=1
    else:
        vote_number = -1
    return vote_number

def update_view_number(view_number, question_id):
    updated_view_number = int(view_number) + 1
    all_questions = questions()
    for dicts in all_questions:
        if dicts["id"] == str(question_id):
            dicts["view_number"] = str(updated_view_number)
    connection.write_data_to_file("question.csv", all_questions, data_header=connection.QUESTION_HEADER)


if __name__ == "__main__":
    edit_answers_question_id(461,462)
