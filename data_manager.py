import connection
import util


def get_question_by_id(id):
    questions = connection.read_data_from_file('question.csv')
    return list(filter(lambda question: question['id'] == str(id), questions)).pop()

def answers_by_question_id(question_id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['question_id'] == str(question_id), answers))

def questions():
    questions = connection.read_data_from_file('question.csv')
    return questions

def add_question(title, message):
    question = {"id": util.create_id(), "submission_time": util.make_timestamp(), "view_number": 0, "vote_number": 0, "title": title, "message": message, "image": None}
    connection.add_data_to_file("question.csv", question, connection.QUESTION_HEADER)
    return question["id"]



if __name__ == "__main__":
    print(questions()[0])
