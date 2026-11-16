"""
TrackMyCourse — Authentication and User Management Blueprint
Handles registration, login, logout, profile updates, and role-based permissions.
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, StudentProfile, StudentEnrollment, University, Program, Scheme, Semester, ActivityLog
from datetime import datetime

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_view"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password. Please try again.", "danger")
            return render_template("auth/login.html", email=email)

        if not user.is_active:
            flash("This account has been deactivated. Please contact an administrator.", "warning")
            return render_template("auth/login.html", email=email)

        login_user(user, remember=remember)
        flash(f"Welcome back, {user.full_name or user.username or 'Scholar'}!", "success")

        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        
        if user.is_admin():
            return redirect(url_for("admin_view"))
        return redirect(url_for("dashboard_view"))

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard_view"))

    universities = University.query.all()
    programs = Program.query.all()

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        university_id = request.form.get("university_id")
        program_id = request.form.get("program_id")

        if not full_name or not email or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("auth/register.html", universities=universities, programs=programs)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html", universities=universities, programs=programs)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("auth/register.html", universities=universities, programs=programs)

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return render_template("auth/register.html", universities=universities, programs=programs)

        if username and User.query.filter_by(username=username).first():
            flash("This username is already taken. Please choose another.", "warning")
            return render_template("auth/register.html", universities=universities, programs=programs)

        # Create new user
        new_user = User(
            email=email,
            username=username or email.split("@")[0],
            full_name=full_name,
            role="student",
            is_active=True
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()

        # Create Profile
        profile = StudentProfile(
            user_id=new_user.id,
            current_semester=1
        )
        db.session.add(profile)

        # Create enrollment if university and program provided
        if university_id and program_id:
            scheme = Scheme.query.filter_by(program_id=program_id).first()
            s_id = scheme.id if scheme else 1
            sem = Semester.query.filter_by(scheme_id=s_id, semester_no=1).first()
            sem_id = sem.id if sem else None

            enrollment = StudentEnrollment(
                user_id=new_user.id,
                university_id=int(university_id),
                program_id=int(program_id),
                scheme_id=s_id,
                current_semester_id=sem_id,
                is_active=True
            )
            db.session.add(enrollment)

        # Log Activity
        log = ActivityLog(
            user_id=new_user.id,
            activity_type="account_registered",
            description=f"Account registered for {full_name}"
        )
        db.session.add(log)
        db.session.commit()

        login_user(new_user)
        flash("Registration successful! Welcome to TrackMyCourse.", "success")
        return redirect(url_for("dashboard_view"))

    return render_template("auth/register.html", universities=universities, programs=programs)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("home_view"))


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    profile = user.profile
    enrollment = StudentEnrollment.query.filter_by(user_id=user.id, is_active=True).first()
    universities = University.query.all()
    programs = Program.query.all()
    schemes = Scheme.query.all()

    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        
        if not profile:
            profile = StudentProfile(user_id=user.id)
            db.session.add(profile)

        profile.enrollment_no = request.form.get("enrollment_no", profile.enrollment_no)
        profile.college_name = request.form.get("college_name", profile.college_name)
        profile.bio = request.form.get("bio", profile.bio)
        
        grad_year = request.form.get("target_graduation_year")
        if grad_year and grad_year.isdigit():
            profile.target_graduation_year = int(grad_year)

        # Update enrollment
        uni_id = request.form.get("university_id")
        prog_id = request.form.get("program_id")
        scheme_id = request.form.get("scheme_id")
        sem_no = request.form.get("current_semester")

        if uni_id and prog_id and scheme_id:
            if not enrollment:
                enrollment = StudentEnrollment(user_id=user.id, is_active=True)
                db.session.add(enrollment)
            enrollment.university_id = int(uni_id)
            enrollment.program_id = int(prog_id)
            enrollment.scheme_id = int(scheme_id)

            if sem_no and sem_no.isdigit():
                profile.current_semester = int(sem_no)
                sem = Semester.query.filter_by(scheme_id=int(scheme_id), semester_no=int(sem_no)).first()
                if sem:
                    enrollment.current_semester_id = sem.id

        # Password change
        new_password = request.form.get("new_password")
        if new_password:
            if len(new_password) < 6:
                flash("New password must be at least 6 characters.", "danger")
            else:
                user.set_password(new_password)
                flash("Password updated successfully.", "success")

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("auth.profile"))

    return render_template(
        "profile.html",
        user=user,
        profile=profile,
        enrollment=enrollment,
        universities=universities,
        programs=programs,
        schemes=schemes
    )


# API: Current user info
@auth.route("/api/me")
def api_me():
    if current_user.is_authenticated:
        enrollment = StudentEnrollment.query.filter_by(user_id=current_user.id, is_active=True).first()
        return jsonify({
            "authenticated": True,
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "university_id": enrollment.university_id if enrollment else 1,
            "program_id": enrollment.program_id if enrollment else 1,
            "scheme_id": enrollment.scheme_id if enrollment else 1,
            "semester_id": enrollment.current_semester_id if enrollment else 1
        })
    else:
        return jsonify({
            "authenticated": False,
            "id": 1,  # Default scholar guest context
            "email": "student@trackmycourse.edu",
            "username": "student",
            "full_name": "Student Scholar",
            "role": "student"
        })
