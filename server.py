from logging import debug
from flask import Flask, render_template, request, redirect
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
    question_list.sort(key=util.sort_by_time, reverse=True)
    for qst in question_list:
        qst['submission_time'] = util.convert_time(qst['submission_time'])
    return render_template("list.html", questions=question_list)


@app.route("/ask-question", methods=["GET", "POST"])
def ask_question():
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        id = data_manager.add_question(title, message)
        return redirect(f"/question/{id}", 301)
    elif request.method == "GET":
        return render_template("ask-question.html")


if __name__ == "__main__":
    app.run(
        debug=True
    )
