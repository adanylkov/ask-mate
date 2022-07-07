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


@app.route("/question/<int:question_id>", methods=['GET', 'POST'])
def display_question(question_id : int):
    if request.method == 'POST':
        req_tag_id = request.values.get('tags-name')
        get_new_tag = request.values.get('create-new-tag')
        data_manager.add_tag_to_question(question_id, req_tag_id)
        data_manager.create_new_tag(get_new_tag)
    data_manager.remove_none_tags()
    current_tags = data_manager.get_tag_for_question(question_id)
    all_tags = data_manager.get_tags()
    question = data_manager.get_question_by_id(question_id)
    question['submission_time'] = util.convert_time(question['submission_time'])
    view_number = (question['view_number'])
    data_manager.update_view_number(view_number, question_id)
    answers = data_manager.answers_by_question_id(question_id)
    comments = data_manager.get_comments_by_question_id(question_id)
    for ans in answers: ans['submission_time'] = util.convert_time(ans['submission_time'])
    for com in comments: com['submission_time'] = util.convert_time(com['submission_time'])
    return render_template("question-template.html", question=question, answers=answers, current_tags=current_tags, question_id=question_id, all_tags=all_tags, comments=comments)


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
        image_name = image()
        id = data_manager.add_question(title, message, image=image_name)
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
        image_name = image()
        data_manager.add_answer(message=message, question_id=question_id, image=image_name)
        return redirect(f"/question/{question_id}", 301)


@app.route("/question/<int:question_id>/delete", methods=['POST'])
def del_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    data_manager.del_question(question)
    return redirect("/", 301)


@app.route("/answer/<int:answer_id>/delete", methods=['POST'])
def del_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = answer['question_id']
    data_manager.del_answer(answer)

    return redirect(url_for('display_question', question_id=question_id))


def image():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return None
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return None
        if file and file.filename and allowed_file(file.filename):
            filename = f"{util.random_identificator()}.{file.filename.rsplit('.', 1)[1]}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"images/{filename}"


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit-question.html', question=question, action=f'/question/{question_id}/edit')
    else:
        title = request.form.get("title")
        message = request.form.get("message")
        image_name = image()
        data_manager.edit_question(question, title, message, image_name)
        return redirect(url_for('display_question', question_id=question['id']), 301)
 

@app.route('/question/<int:question_id>/vote-up', methods = ['POST'])
def vote_up(question_id):
    question = data_manager.get_question_by_id(question_id)
    vote_number = int(question['vote_number'])
    updated_vote_number = data_manager.vote_up(vote_number)
    data_manager.vote_update(updated_vote_number, question_id)
    return redirect("/", 301)


@app.route('/question/<int:question_id>/vote-down', methods = ['POST'])
def vote_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    vote_number = int(question['vote_number'])
    updated_vote_number = data_manager.vote_down(vote_number)
    data_manager.vote_update(updated_vote_number, question_id)
    return redirect("/", 301)


@app.route('/answer/<int:answer_id>/vote-up', methods = ['POST'])
def vote_up_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    vote_number = int(answer['vote_number'])
    updated_vote_number = data_manager.vote_up(vote_number)
    answer['vote_number'] = updated_vote_number
    id = data_manager.edit_answer(answer)
    return redirect(f"/question/{id}", 301)


@app.route('/answer/<int:answer_id>/vote-down', methods = ['POST'])
def vote_down_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    vote_number = int(answer['vote_number'])
    updated_vote_number = data_manager.vote_down(vote_number)
    answer['vote_number'] = updated_vote_number
    id = data_manager.edit_answer(answer)
    return redirect(f"/question/{id}", 301)


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def new_tag(question_id):
    if request.method == 'POST':
        return redirect(f'/question/{question_id}/new-tag', 301)
    current_tags = data_manager.get_tags()
    data_manager.remove_none_tags()
    return render_template('question-new-tag.html', id=question_id, current_tags=current_tags)


@app.route('/question/<int:question_id>/tag/<int:tag_id>/delete', methods=['GET', 'POST'])
def remove_tag_from_question(question_id, tag_id):
    data_manager.remove_tag(question_id, tag_id)
    return redirect (f'/question/{question_id}', 301)


@app.route('/answer/<int:answer_id>/new-comment', methods = ['GET', 'POST'])
@app.route('/question/<int:question_id>/new-comment', methods = ['GET', 'POST'])
def add_comment(question_id = None, answer_id = None):
    if request.method == 'GET':
        return render_template('add-comment.html')
    else:
        comment = {
                'message': request.form.get('message'),
                'question_id': question_id,
                'answer_id': answer_id,
                'submission_time': util.make_timestamp()
                }
        if question_id is None:
            question_id = data_manager.get_question_id_by_answer_id(answer_id)
            comment['question_id'] = question_id
        data_manager.add_comment(comment)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/comment/<int:comment_id>/edit', methods = ['GET', 'POST'])
def edit_comment(comment_id: int):
    comment = data_manager.get_comment_by_id(comment_id)
    if request.method == 'GET':
        return render_template('edit-comment.html', comment=comment)
    else:
        comment['message'] = request.form.get('message')
        comment['edited_count'] = 1 if not comment['edited_count'] else comment['edited_count'] + 1
        data_manager.edit_comment(comment)
        question_id = comment.get('question_id')
        if question_id is None: 
            question_id = data_manager.get_question_id_by_answer_id(comment.get('answer_id'))
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/comment/<int:comment_id>/delete', methods = ['POST'])
def delete_comment(comment_id: int):
    question_id = data_manager.delete_comment(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/search')
def search():
    search_for = request.args.get('q')
    search_result = data_manager.search(search_for)
    return render_template('search.html', search_result=search_result, search_for=search_for)


if __name__ == "__main__":
    app.run(
        debug = True
    )
    
