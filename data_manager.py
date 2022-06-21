import connection


def get_question_by_id(id):
    questions = connection.read_data_from_file('question.csv')
    return list(filter(lambda question: question['id'] == str(id), questions)).pop()

def answers_by_question_id(question_id):
    answers = connection.read_data_from_file('answer.csv')
    return list(filter(lambda answer: answer['question_id'] == str(question_id), answers))

def questions():
    questions = connection.read_data_from_file('question.csv')
    
    return questions


if __name__ == "__main__":
    print(questions()[0])
