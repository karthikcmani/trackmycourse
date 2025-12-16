from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# ---------- USER ----------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


# ---------- ACADEMIC STRUCTURE ----------

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey("university.id"))


class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))


class Scheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(10), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    stream_id = db.Column(db.Integer, db.ForeignKey("stream.id"), nullable=True)


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semester_no = db.Column(db.Integer, nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey("scheme.id"))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semester.id"))


# ---------- SYLLABUS ----------

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    hours = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

    topics = db.relationship("Topic", backref="module", lazy=True)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)


# ---------- USER PROGRESS ----------

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))
    completed = db.Column(db.Boolean, default=False)
