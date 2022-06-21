from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return '''
            <p>Hello world!</p>
            <br>
            <a href="http://127.0.0.1:5000/list">Click here to go to the list of questions :)</a>'''

@app.route("/list")
def list():
    return "Hello stranger!"

@app.route("/question/<question_id>")
def display_question(question_id):
    return render_template('index.html')

@app.route("/question/<question_id>/new-answer")
def post_an_answer(question_id):
    return render_template('post_an_answer.html')

@app.route("/question/<question_id>/edit")
def edit_question(question_id):
    return render_template('edit_question.html')

if __name__ == "__main__":
    app.run()
