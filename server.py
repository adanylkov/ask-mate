from logging import debug
from flask import Flask, render_template
import data_manager
import util

app = Flask(__name__)


@app.route("/question/<int:question_id>")
def display_question(question_id):

    question = data_manager.get_question_by_id(question_id)
    question['submission_time'] = util.convert_time(question['submission_time'])
    answers = data_manager.answers_by_question_id(question_id)
    for ans in answers:
        ans['submission_time'] = util.convert_time(ans['submission_time'])
    return render_template("question.html", question=question, answers=answers)

@app.route("/")
@app.route("/list")
def question_list():
    question_list = data_manager.questions()
    print(sorted(question_list, key=util.sort_by_time, reverse=True))
    for qst in sorted(question_list, key=util.sort_by_time, reverse=True):
        qst['submission_time'] = util.convert_time(qst['submission_time'])
    return render_template("list.html", questions=question_list)


if __name__ == "__main__":
    app.run(
        debug = True
    )
    
