import os
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "6ywhzzfBKxEg%qHxUDT8#"

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    email = db.Column(db.String(200))

    def __init__(self, name, city, email):
        self.name = name
        self.city = city
        self.email = email


@app.route('/')
def show_all():
    students = Student.query.all()
    return render_template('show_all.html', students=students)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        try:
            student = Student(
                request.form['name'], request.form['city'], request.form['email'])

            db.session.add(student)
            db.session.commit()
            return redirect(url_for('show_all'))
        except:
            redirect(url_for('new'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
