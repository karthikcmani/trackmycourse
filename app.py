from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from api import api   # import blueprint ONLY

# ---------- CREATE APP ----------
app = Flask(__name__)
app.secret_key = "super-secret-key"

# ---------- DATABASE ----------
import os

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "trackmycourse.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

os.makedirs(app.instance_path, exist_ok=True)
db.init_app(app)

# ---------- LOGIN ----------
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- REGISTER API (ONLY HERE) ----------
app.register_blueprint(api)

# ---------- ROUTES ----------
@app.route("/")
def home():
    return "TrackMyCourse backend running 🚀"

@app.route("/ui")
def ui():
    return render_template("index.html")

# ---------- INIT DB ----------
with app.app_context():
    db.create_all()

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
