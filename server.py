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



if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
