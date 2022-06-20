from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"



@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
    return render_template('add-question.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
