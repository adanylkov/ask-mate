from flask import Flask, render_template, request, redirect, flash, url_for
import data_manager
import util
import os

UPLOAD_FOLDER = 'static/images/'
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
    view_number = (question['view_number'])
    data_manager.update_view_number(view_number, question_id)
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
        id = util.create_id()
        image_name = image(question_id=id)
        if image_name:
            image_name = f"images/{image_name}"
        data_manager.add_question(title, message, id=id, image=image_name)
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
        answer_id = util.create_id(is_question=False)
        image_name = image(question_id=question_id, answer_id=str(answer_id))
        if image_name:
            image_name = f"images/{image_name}"
        data_manager.add_answer(question_id=question_id, message=message, id=answer_id, image=image_name)
        return redirect(f"/question/{question_id}", 301)


@app.route("/question/<int:question_id>/delete")
def del_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.del_question(question, edit=False)
    return redirect("/", 301)


@app.route("/answer/<int:answer_id>/delete")
def del_answer(answer_id):
    question_id = data_manager.del_answer(answer_id)
    return redirect(f"/question/{question_id}", 301)


def image(question_id, answer_id=''):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return None
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return None
        if file and file.filename and allowed_file(file.filename):
            filename = f"{question_id}_{answer_id}.{file.filename.rsplit('.', 1)[1]}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit-question.html', question=question, action=f'/question/{question_id}/edit')
    else:
        title = request.form.get("title")
        message = request.form.get("message")
        question['title'] = title
        question['message'] = message
        question['new_id'] = util.create_id()
        image_name = image(question_id=question['new_id'])
        if image_name:
            question['image'] = f"images/{image_name}"
        data_manager.edit_question(question)
        return redirect(url_for('display_question', question_id=question['new_id']), 301)
 

@app.route('/question/<int:question_id>/vote-up')
def vote_up(question_id):
    question = data_manager.get_question_by_id(question_id)
    vote_number = int(question['vote_number'])
    updated_vote_number = data_manager.vote_up(vote_number)
    question['vote_number'] = updated_vote_number
    id = util.create_id()
    question['new_id'] = id
    data_manager.edit_question(question)
    return redirect("/", 301)

@app.route('/question/<int:question_id>/vote-down')
def vote_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    vote_number = int(question['vote_number'])
    updated_vote_number = data_manager.vote_down(vote_number)
    question['vote_number'] = updated_vote_number
    id = util.create_id()
    question['new_id'] = id
    data_manager.edit_question(question)
    return redirect("/", 301)



if __name__ == "__main__":
    app.run(
        debug = True
    )
    
