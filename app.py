"""
TrackMyCourse — Production Academic Progress Management Platform
Flask Application Factory & Route Dispatcher
"""
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user, login_required
from models import db, User

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    secret_key = os.environ.get("SECRET_KEY", "trackmycourse-production-secret-2026")
    app.config["SECRET_KEY"] = secret_key

    # Database
    db_path = os.path.join(app.instance_path, "trackmycourse.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", f"sqlite:///{db_path}")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Maximum upload size: 16 MB
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, "uploads"), exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Authentication setup
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access your personal academic workspace."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from auth import auth as auth_blueprint
    from api import api as api_blueprint
    from study_api import study_api as study_blueprint
    from analytics_api import analytics_api as analytics_blueprint
    from admin_api import admin_api as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(study_blueprint)
    app.register_blueprint(analytics_blueprint)
    app.register_blueprint(admin_blueprint)

    # Web View Routes
    @app.route("/")
    def home_view():
        return render_template("home.html", active_page="home")

    @app.route("/dashboard")
    def dashboard_view():
        return render_template("dashboard.html", active_page="dashboard")

    @app.route("/progress")
    def progress_view():
        # Preserved core syllabus progress tracking experience
        return render_template("index.html", active_page="progress")

    @app.route("/ui")
    def legacy_ui_redirect():
        # Backward compatibility for existing bookmarks
        return redirect(url_for("progress_view"))

    @app.route("/academics")
    def academics_view():
        return render_template("academics.html", active_page="academics")

    @app.route("/planner")
    def planner_view():
        return render_template("planner.html", active_page="planner")

    @app.route("/notes")
    def notes_view():
        return render_template("notes.html", active_page="notes")

    @app.route("/resources")
    def resources_view():
        return render_template("resources.html", active_page="resources")

    @app.route("/goals")
    def goals_view():
        return render_template("goals.html", active_page="goals")

    @app.route("/analytics")
    def analytics_view():
        return render_template("analytics.html", active_page="analytics")

    @app.route("/admin")
    def admin_view():
        return render_template("admin/admin.html", active_page="admin")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
