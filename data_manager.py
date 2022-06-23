import connection
import util
import os


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


def get_question_by_id(id):
    questions = connection.read_data_from_file('question.csv')
    return list(filter(lambda question: question['id'] == str(id), questions)).pop()

def answers_by_question_id(question_id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['question_id'] == str(question_id), answers))

def questions():
    questions = connection.read_data_from_file('question.csv')
    return questions

def answers():
    answers = connection.read_data_from_file('answer.csv')
    return answers

def add_question(title, message, id = None, submission_time = None, view_number = None, vote_number = None, image = None):
    question = {
            "id": util.create_id() if not id else id,
            "submission_time": util.make_timestamp() if not submission_time else submission_time,
            "view_number": 0 if not view_number else view_number,
            "vote_number": 0 if not vote_number else vote_number,
            "title": title,
            "message": message,
            "image": None if not image else image
            }
    connection.add_data_to_file("question.csv", question, connection.QUESTION_HEADER)
    return question["id"]

def add_answer(question_id, message, id = None, image = None):
    #id,submission_time,vote_number,question_id,message,image
    answer = {
            "id": util.create_id(is_question=False) if not id else id,
            "submission_time": util.make_timestamp(),
            "vote_number": 0,
            "question_id": question_id,
            "message": message,
            "image": None if not image else image,
            }
    connection.add_data_to_file('answer.csv', data=answer, data_header=connection.ANSWER_HEADER)

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


def del_answer(answer_id):
    all_answers = answers()
    for dicts in all_answers:
        if dicts["id"] == str(answer_id):
            delete_image(dicts)
            all_answers.pop(all_answers.index(dicts))
            question_id = dicts["question_id"]
            connection.write_data_to_file("answer.csv", all_answers, data_header=connection.ANSWER_HEADER)
            return question_id


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

if __name__ == "__main__":
    edit_answers_question_id(461,462)
