from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import  os, connection, util
UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
question_path = "sample_data/question.csv"
answer_path = "sample_data/answer.csv"
question_keys = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
TABLE_HEADERS = ["ID", "DATE", "View", "Vote", "Title", "Message", "Image"]


@app.route("/")
@app.route("/list")
def question_list():
    all_stats = connection.reader_csv(question_path)
    questions_with_timestamp = util.get_date_format(all_stats)
    return render_template("index.html", questions_with_timestamp=questions_with_timestamp, TABLE_HEADERS=TABLE_HEADERS)


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
        return redirect("/list")
    return render_template('add-question.html')


@app.route("/question/<int:question_id>", methods=["GET", "POST"])
def display_question(question_id):
    questions = connection.reader_csv(question_path)
    # question_title = questions[question_id-1]["title"]
    # question_message = questions[question_id-1]["message"]
    answers = connection.reader_csv(answer_path)

    # for answer in answers:
    #     if answer["question_id"] == str(question_id):
    #         question_answers.append(answer["message"])
    if request.method =="POST":
        return redirect(url_for("new_answer", question_id=question_id))
    return render_template("display_question.html", question_id=question_id, questions=questions,answers=answers)
    
    
@app.route("/question/<question_id>/delete")
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
    title_message = request.form.get("message")
    if request.method == "POST":
        answer_id = util.generate_new_id("last_answer_id.txt")

        new_answer_dict = {"id": answer_id, "submission_time": 0, "vote_number": 0, "question_id": question_id,
                       "message": title_message, "image": ""}

        connection.write_data(new_answer_dict, answer_path)
        return redirect(url_for("display_question",question_id=question_id))
    question = connection.reader_csv(question_path)
    question_title = question[question_id - 1]["title"]
    question_message = question[question_id - 1]["message"]

    return render_template("new_answer.html", question_title=question_title, question_message=question_message,title_message=title_message, question_id=question_id)


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == 'POST':
        edited_question = {
            "id": question_id,
            "submission_time": util.get_current_time(),
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get("title"),
            "message": request.form.get("message"),
        }
        questions = connection.update_question(edited_question, question_id)

        return redirect(url_for("display_question", question_id=question_id))
    else:
        data = connection.reader_csv(question_path)
        return render_template("edit_question.html", question_id=question_id, questions=data)


@app.route("/list/sorted")
def sorted_list():
    title = sorted(questions_with_timestamp,key = lambda i: (i["title"]).lower())
    title_reverse = sorted(questions_with_timestamp,key = lambda i: (i["title"]).lower(), reverse=True)
    submission_time = sorted(questions_with_timestamp,key = lambda i: i["submission_time"])
    submission_time_reverse = sorted(questions_with_timestamp,key = lambda i:i["submission_time"], reverse=True)
    message = sorted(questions_with_timestamp,key = lambda i: (i["message"]).lower())
    message_reverse = sorted(questions_with_timestamp,key = lambda i: (i["message"]).lower(), reverse=True)
    view_number = sorted(questions_with_timestamp,key = lambda i: int(i["view_number"]))
    view_number_reverse = sorted(questions_with_timestamp,key = lambda i: int(i["view_number"]), reverse=True)
    vote_number = sorted(questions_with_timestamp,key = lambda i: int(i["vote_number"]))
    vote_number_reverse = sorted(questions_with_timestamp,key = lambda i: int(i["vote_number"]), reverse=True)
    return render_template("sorted.html", TABLE_HEADERS=TABLE_HEADERS, submission_time=submission_time, submission_time_reverse=submission_time_reverse, title=title, title_reverse=title_reverse, message=message,message_reverse=message_reverse, view_number=view_number, view_number_reverse=view_number_reverse,  vote_number=vote_number, vote_number_reverse=vote_number_reverse)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
