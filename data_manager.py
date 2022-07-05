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
    image_name = question.get('image')
    if not image_name: return
    image_folder = os.path.join(os.curdir, 'static')
    image_file = os.path.join(image_folder, image_name)
    if os.path.isfile(image_file):
        os.remove(image_file)



@database_common.connection_handler
def get_question_by_id(cursor, id):
    query = """
        SELECT *
        FROM question
        WHERE id = %s
        """
    cursor.execute(query, (id, ))
    questions = cursor.fetchall()
    question = list(map(util.question_datetime_to_epoch, questions))
    return question.pop() if question else None 

@database_common.connection_handler
def get_answer_by_id(cursor, id):
    query = """
    SELECT *
    FROM answer
    WHERE id = %s
    """
    cursor.execute(query, (id,))
    return cursor.fetchone()

@database_common.connection_handler
def answers_by_question_id(cursor, question_id):
    query = """
    SELECT *
    FROM answer
    WHERE question_id = %s
    ORDER BY vote_number DESC
    """
    cursor.execute(query, (question_id, ))
    answers = cursor.fetchall()
    return list(map(util.question_datetime_to_epoch, answers))


@database_common.connection_handler
def questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC 
        LIMIT 5
        """
    cursor.execute(query)
    questions = cursor.fetchall()
    return list(map(util.question_datetime_to_epoch, questions))
#
#     questions = connection.read_data_from_file('question.csv')
#     return questions

@database_common.connection_handler
def answers(cursor):
    query = """
        SELECT *
        FROM answer
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question(cursor, title, message, submission_time = None, view_number = None, vote_number = None, image = None):
    question = {
            "submission_time": util.make_timestamp(),
            "view_number": 0 if not view_number else view_number,
            "vote_number": 0 if not vote_number else vote_number,
            "title": title,
            "message": message,
            "image": image
            }
    #connection.add_data_to_file("question.csv", question, connection.QUESTION_HEADER)
    cursor.execute("""INSERT INTO question
            (submission_time, view_number, vote_number, title, message, image)
            VALUES (%(s_t)s, %(vi_n)s, %(vo_n)s, %(t_l)s, %(m_g)s, %(i_g)s)""",
                   {'s_t': question['submission_time'],
                    'vi_n': question['view_number'],
                    'vo_n': question['vote_number'],
                    't_l': question['title'],
                    'm_g': question['message'],
                    'i_g': question['image']
                    })
    query = """SELECT id FROM question ORDER BY id DESC LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchone().get('id')



@database_common.connection_handler
def add_answer(cursor, message, question_id, image = None):
    answer = {
            "submission_time": util.make_timestamp(),
            "vote_number": 0,
            "question_id": question_id,
            "message": message, 
            "image": image
            }
    query = """
    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, [value for value in answer.values()])


@database_common.connection_handler
def del_question(cursor, question):
    query = """
    SELECT * FROM answer
    WHERE question_id = %s
    """
    cursor.execute(query, (question['id'], ))
    answers = cursor.fetchall()
    answers.append(question)
    for id in answers:
        delete_image(id)

    query = """
    DELETE FROM answer
    WHERE question_id = %s
    """
    cursor.execute(query, (question['id'],))
    query = """
    DELETE FROM question
    WHERE id = %s
    """
    cursor.execute(query, (question['id'],))


@database_common.connection_handler
def del_answer(cursor, answer):
    delete_image(answer)
    answer_id = answer['id']
    query = """
    DELETE 
    FROM answer
    WHERE id = %s
    """
    cursor.execute(query, (answer_id, ))


def edit_answers_question_id(question_id, new_id):
    all_answers = connection.read_data_from_file('answer.csv')
    for answer in all_answers:
        if answer['question_id'] == str(question_id):
            answer['question_id'] = str(new_id)
    connection.write_data_to_file('answer.csv', data=all_answers, data_header=connection.ANSWER_HEADER)


@database_common.connection_handler
def edit_question(cursor, question, title, message, image_name):
    query = """
    UPDATE question
        SET title = %s, message = %s, image = %s
        WHERE id = %s
    """
    if image_name:
        delete_image(question)
    cursor.execute(query, (title, message, image_name if image_name else question['image'], question['id']))


@database_common.connection_handler
def edit_answer(cursor, answer):
        query = """
        UPDATE answer
            SET vote_number = %s, message = %s, image = %s
            WHERE id = %s
        """
        cursor.execute(query, (answer['vote_number'], answer['message'], answer['image'], answer['id']))
        return answer['question_id']

@database_common.connection_handler
def vote_update(cursor, updated_vote_number, question_id):
    query = """
        UPDATE question
            SET vote_number = %s
            WHERE id = %s
        """
    cursor.execute(query, (updated_vote_number, question_id))

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


@database_common.connection_handler
def update_view_number(cursor, view_number, question_id):
    updated_view_number = int(view_number) + 1
    # all_questions = questions()
    # for dicts in all_questions:
    #     if dicts["id"] == str(question_id):
    #         dicts["view_number"] = str(updated_view_number)
    # connection.write_data_to_file("question.csv", all_questions, data_header=connection.QUESTION_HEADER)
    query = """
    UPDATE question
        SET view_number = %s
        WHERE id = %s
    """
    cursor.execute(query, (updated_view_number, question_id))


if __name__ == "__main__":
    edit_answers_question_id(461,462)
