from flask import Flask, render_template
import data_manager
import util

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/question/<int:question_id>")
def display_question(question_id):

    question = data_manager.get_question_by_id(question_id)
    question['submission_time'] = util.convert_time(question['submission_time'])
    answers = data_manager.answers_by_question_id(question_id)
    for ans in answers:
        ans['submission_time'] = util.convert_time(ans['submission_time'])
    return render_template("question.html", question=question, answers=answers)


if __name__ == "__main__":
    app.run()
