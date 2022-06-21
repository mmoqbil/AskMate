from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import  os, connection, util

app = Flask(__name__)
question_path = "sample_data/question.csv"
answer_path = "sample_data/answer.csv"
question_keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/list")
def question_list():
    TABLE_HEADERS = ["ID", "DATE", "View", "Vote", "Title", "Message", "Image"]
    all_stats = connection.reader_csv(question_path)
    return render_template("question_list.html", all_stats=all_stats, TABLE_HEADERS=TABLE_HEADERS)

@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        image_path = None
        if request.files['image']:
            filename = secure_filename(request.files['image'].filename)
            request.files['image'].save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = 'static/images/%s' % filename

        connection.writer_csv(question_path, question_keys, util.create_fields(title, question, image_path))
    return render_template('add-question.html')

@app.route("/question/<int:question_id>")
def display_question(question_id):
    question = connection.reader_csv(question_path)
    question_title = question[question_id-1]["title"]
    question_message = question[question_id-1]["message"]
    return render_template("display_question.html", question_title = question_title, question_message = question_message)
@app.route("/question/<question_id>/delete", methods=["POST", "GET"])
def delete_question(question_id):
    connection.delete_question(question_id)
    return redirect("/list")
@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = request.args.get("question_id")
    connection.delete_answer(answer_id)
    return redirect(url_for("display_question", question_id=question_id))
@app.route("/question/<int:question_id>/new_answer", methods = ["POST", "GET"])
def new_answer(question_id):
    question = connection.reader_csv(question_path)
    question_title = question[question_id - 1]["title"]
    question_message = question[question_id - 1]["message"]
    title_message = request.form.get("message")
    answer_id = util.generate_new_id("last_answer_id.txt")
    new_answer_dict = {"id":answer_id, "submission_time":0, "vote_number":0, "question_id":question_id, "message":title_message, "image":""}
    connection.write_data(new_answer_dict, answer_path)
    return render_template("new_answer.html", question_title=question_title, question_message=question_message,title_message=title_message, question_id=question_id)



if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
