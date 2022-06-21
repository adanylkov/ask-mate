from flask import Flask, render_template, request
from connection import add_data_to_file
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add-question", methods=["GET","POST"])
def ask_question():
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        my_list = {'id': 81,'submission_time': 123123,'view_number':1,'vote_number':2,'title':title, 'message':message, 'image':'None'}
        add_data_to_file("question.csv", my_list, connection.QUESTION_HEADER)
        return render_template("add-question.html")
    # return render_template("add-question.html")
    # id,submission_time,view_number,vote_number,title,message,image


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
