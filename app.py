from flask import Flask, render_template
from models import db
from api import api
from file_browser import file_api

app = Flask(__name__)

app.secret_key = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trackmycourse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# REGISTER BLUEPRINTS
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(file_api, url_prefix="/api")

@app.route("/")
def home():
    return "TrackMyCourse backend running 🚀"

@app.route("/ui")
def ui():
    return render_template("index.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
