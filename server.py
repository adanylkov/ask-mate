#from rich import print
#from logging import debug
from flask import Flask, render_template, request, redirect, flash, url_for
#from flask import send_from_directory
from werkzeug.utils import secure_filename
import data_manager
import util
import os

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/question/<int:question_id>")
def display_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    question['submission_time'] = util.convert_time(question['submission_time'])
    answers = data_manager.answers_by_question_id(question_id)
    for ans in answers:
        ans['submission_time'] = util.convert_time(ans['submission_time'])
    return render_template("question-template.html", question=question, answers=answers)


@app.route("/")
@app.route("/list")
def question_list():
    question_list = data_manager.questions()


    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'desc')

    question_list.sort(key=lambda question: util.sort_by(question, order_by), reverse=order_direction=='desc') 

    for qst in question_list:
        qst['submission_time'] = util.convert_time(qst['submission_time'])
    return render_template("list.html", questions=question_list)


@app.route("/ask-question", methods=["GET", "POST"])
def ask_question():
    if request.method=="POST":
        title = request.form.get("title")
        message = request.form.get("message")
        id = data_manager.add_question(title, message)
        return redirect(f"/question/{id}", 301)
    elif request.method=="GET":
        return render_template("ask-question.html")

    
@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def get_answer(question_id):
    if request.method == "GET":
        question = data_manager.get_question_by_id(question_id)
        question['submission_time'] = util.convert_time(question['submission_time'])
        return render_template("answer-question.html", question=question)
    else:
        message = request.form.get("message")
        data_manager.add_answer(question_id=question_id, message=message)
        return redirect(f"/question/{question_id}", 301)


@app.route("/question/<int:question_id>/delete")
def del_question(question_id):
    data_manager.del_question(question_id)
    return redirect("/", 301)


@app.route("/answer/<int:answer_id>/delete")
def del_answer(answer_id):
    question_id = data_manager.del_answer(answer_id)
    return redirect(f"/question/{question_id}", 301)


@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        app.logger.debug("Got POST request")
        # check if the post request has the file part
        if 'image' not in request.files:
            app.logger.error("No file part")
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            app.logger.error("No selected file")
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename and allowed_file(file.filename):
            app.logger.debug("Trying to save file")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('question_list'))

    else:
        return render_template("image.html")


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit-question.html', question=question, action=f'/question/{question_id}/edit')
    else:
        print("in edit_question POST")
        title = request.form.get("title")
        message = request.form.get("message")
        question['title'] = title
        question['message'] = message
        id = data_manager.edit_question(question)
        return redirect(url_for('display_question', question_id=id), 301)
 

@app.route('/question/<int:question_id>/vote-up')
def vote_up(question_id):
    question = data_manager.get_question_by_id(question_id)
    vote_number = int(question['vote_number'])
    updated_vote_number = data_manager.vote_up(vote_number)
    question['vote_number'] = updated_vote_number
    id = data_manager.edit_question(question)
    return redirect("/", 301)

@app.route('/question/<int:question_id>/vote-down')
def vote_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    vote_number = int(question['vote_number'])
    updated_vote_number = data_manager.vote_down(vote_number)
    question['vote_number'] = updated_vote_number
    id = data_manager.edit_question(question)
    return redirect("/", 301)

#answer
@app.route('/answer/<int:answer_id>/vote-up')
def vote_up_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    print(answer)
    vote_number = int(answer['vote_number'])
    updated_vote_number = data_manager.vote_up(vote_number)
    answer['vote_number'] = updated_vote_number
    id = data_manager.edit_answer(answer)
    return redirect(f"/question/{id}", 301)


@app.route('/answer/<int:answer_id>/vote-down')
def vote_down_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    vote_number = int(answer['vote_number'])
    updated_vote_number = data_manager.vote_down(vote_number)
    answer['vote_number'] = updated_vote_number
    id = data_manager.edit_answer(answer)
    return redirect(f"/question/{id}", 301)


if __name__ == "__main__":
    app.run(
        debug = True
    )
    
