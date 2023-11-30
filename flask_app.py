#  source venv/bin/activate
from flask import Flask, render_template, flash, request, redirect
from flask_bootstrap import Bootstrap
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
Bootstrap(app)
# CKEditor(app)

app.config['SECRET_KEY'] = os.urandom(24)

# DB Config

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="  пароль",
    hostname="localhost",
    databasename="comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    text = db.Column(db.String(1000))

    # def __repr__(self):
    #     return [self.name, self.text]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/feedbacks')
def feedbacks():
    comments = Comment.query.all()
    if comments:
        return render_template("feedbacks.html", comments=comments)
    else:
        return render_template("feedbacks.html", comments=None)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        if not request.form["name"] or not request.form["text"]:
            flash("Поля не должны быть пустыми.", 'danger')
            # return render_template("feedback.html")
        else:
            comment = Comment(
                name=request.form["name"], text=request.form["text"])
            db.session.add(comment)
            db.session.commit()
            return redirect('/feedbacks')
    return render_template("feedback.html")


if (__name__ == '__main__'):
    app.run(debug=True)
