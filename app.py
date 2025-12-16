from flask import Flask
from flask_login import LoginManager
from models import db, User
from api import api   # ✅ THIS LINE MUST EXIST

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trackmycourse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ✅ REGISTER API BLUEPRINT
app.register_blueprint(api)


@app.route("/")
def home():
    return "TrackMyCourse backend running 🚀"


# Flask 3.x DB init
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
