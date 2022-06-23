import connection
import util


def get_question_by_id(id):
    questions = connection.read_data_from_file('question.csv')
    return list(filter(lambda question: question['id'] == str(id), questions)).pop()

def get_answer_by_id(id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['id'] == str(id), answers)).pop()

def answers_by_question_id(question_id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['question_id'] == str(question_id), answers))

def questions():
    questions = connection.read_data_from_file('question.csv')
    return questions

def answers():
    answers = connection.read_data_from_file('answer.csv')
    return answers

def add_question(title, message, submission_time = None, view_number = None, vote_number = None, image = None):
    question = {
            "id": util.create_id(),
            "submission_time": util.make_timestamp() if not submission_time else submission_time,
            "view_number": 0 if not view_number else view_number,
            "vote_number": 0 if not vote_number else vote_number,
            "title": title,
            "message": message,
            "image": None if not image else image
            }
    connection.add_data_to_file("question.csv", question, connection.QUESTION_HEADER)
    return question["id"]

def add_answer(message, question_id, submission_time = None, vote_number = None, image = None):
    #id,submission_time,vote_number,question_id,message,image
    answer = {
            "question_id": question_id,
            "id": util.create_id(), 
            "submission_time": util.make_timestamp() if not submission_time else submission_time, 
            "vote_number": 0 if not vote_number else vote_number, 
            "message": message, 
            "image": None if not image else image}
    connection.add_data_to_file('answer.csv', data=answer, data_header=connection.ANSWER_HEADER)


def del_question(question_id):
    all_answers = answers()
    all_questions = questions()
    for dicts in all_questions:
        if dicts["id"] == str(question_id):
            all_questions.pop(all_questions.index(dicts))
    connection.write_data_to_file("question.csv", all_questions, data_header=connection.QUESTION_HEADER)
    for dicts in all_answers:
        if dicts["question_id"] == str(question_id):
            all_answers.pop(all_answers.index(dicts))
    connection.write_data_to_file("answer.csv", all_answers, data_header=connection.ANSWER_HEADER)


def del_answer(answer_id):
    all_answers = answers()
    for dicts in all_answers:
        if dicts["id"] == str(answer_id):
            index = all_answers.index(dicts)
            all_answers.pop(index)
            question_id = dicts["question_id"]
            connection.write_data_to_file("answer.csv", all_answers, data_header=connection.ANSWER_HEADER)
            return question_id, index


def edit_question(question):
    del_question(question['id'])
    id = add_question(
            title=question['title'],
            submission_time=question['submission_time'],
            message=question['message'],
            view_number=question['view_number'],
            vote_number=question['vote_number'],
            image=question['image']
            )
    return id


def edit_answer(answer):
    delete_question = del_answer(answer['id'])
    index = delete_question[1]
    add_answer(
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

if __name__ == "__main__":
    print(questions()[0])
