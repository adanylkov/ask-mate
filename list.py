from flask import Flask
import csv

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

DATA_HEADER = ["id","submission_time","view_number","vote_number","title","message","image"]


def read():
    with open("sample_data/question.csv", 'r') as file:
        reader = csv.DictReader(file)
        questions = []
        for question in reader:
            questions.append(question)
        return questions

# def write():
#     with open("sample_data/question.csv", 'w') as file:
#                 writer = csv.DictWriter(file, DATA_HEADER)
#                 # questions.pop(int(question['id']) - 1)
#                 # questions.insert(int(question['id']) - 1, question)
#                 writer.writeheader()
#                 writer.writerows(questions)

list_of_questions = read()
print(list_of_questions)

if __name__ == "__main__":
    app.run()