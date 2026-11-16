"""
TrackMyCourse — Analytics & Academic Insights Engine
Computes real progress, syllabus completion, study time metrics, and activity history.
Zero fake data; all numbers are calculated from database records.
"""
from flask import Blueprint, jsonify
from flask_login import current_user
from models import (
    db,
    Course,
    Module,
    Topic,
    UserProgress,
    StudySession,
    StudyTask,
    StudentEnrollment,
    ActivityLog,
    Semester
)
from datetime import datetime, date, timedelta

analytics_api = Blueprint("analytics_api", __name__, url_prefix="/api/analytics")

def get_current_user_id():
    return current_user.id if current_user.is_authenticated else 1


@analytics_api.route("/dashboard")
def dashboard_stats():
    """
    Computes genuine student progress and dashboard metrics from database.
    """
    user_id = get_current_user_id()

    # Get student enrollment
    enrollment = StudentEnrollment.query.filter_by(user_id=user_id, is_active=True).first()

    target_scheme_id = enrollment.scheme_id if enrollment else 1
    target_semester_id = enrollment.current_semester_id if enrollment else 1

    # Get courses for this semester
    courses = Course.query.filter_by(semester_id=target_semester_id).all()
    if not courses:
        # Fallback to all courses in scheme if semester has none
        courses = Course.query.join(Semester).filter(Semester.scheme_id == target_scheme_id).all()

    total_topics_all = 0
    completed_topics_all = 0
    course_cards = []

    for c in courses:
        c_topics = (
            Topic.query
            .join(Module, Topic.module_id == Module.id)
            .filter(Module.course_id == c.id)
            .count()
        )
        c_completed = (
            UserProgress.query
            .join(Topic, UserProgress.topic_id == Topic.id)
            .join(Module, Topic.module_id == Module.id)
            .filter(
                Module.course_id == c.id,
                UserProgress.user_id == user_id,
                UserProgress.completed == True
            )
            .count()
        )

        c_percent = round((c_completed / c_topics * 100), 1) if c_topics > 0 else 0.0

        total_topics_all += c_topics
        completed_topics_all += c_completed

        course_cards.append({
            "id": c.id,
            "name": c.name,
            "code": c.code or f"CRS-{c.id}",
            "credits": c.credits or 4,
            "course_type": c.course_type or "Theory",
            "total_topics": c_topics,
            "completed_topics": c_completed,
            "remaining_topics": max(0, c_topics - c_completed),
            "percentage": c_percent
        })

    overall_percent = (
        round((completed_topics_all / total_topics_all * 100), 1)
        if total_topics_all > 0 else 0.0
    )

    # Study time calculations
    total_study_minutes = (
        db.session.query(db.func.sum(StudySession.duration_minutes))
        .filter(StudySession.user_id == user_id)
        .scalar() or 0
    )

    # Study tasks summary
    pending_tasks = StudyTask.query.filter_by(user_id=user_id, status="pending").count()
    completed_tasks = StudyTask.query.filter_by(user_id=user_id, status="completed").count()

    # Recent activities
    recent_activities = (
        ActivityLog.query
        .filter_by(user_id=user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )

    # Weekly study activity (last 7 days)
    today = date.today()
    weekly_data = []
    for day_offset in range(6, -1, -1):
        day = today - timedelta(days=day_offset)
        day_minutes = (
            db.session.query(db.func.sum(StudySession.duration_minutes))
            .filter(StudySession.user_id == user_id, StudySession.session_date == day)
            .scalar() or 0
        )
        weekly_data.append({
            "date": day.strftime("%a %d"),
            "minutes": day_minutes
        })

    return jsonify({
        "overall_percentage": overall_percent,
        "total_topics": total_topics_all,
        "completed_topics": completed_topics_all,
        "remaining_topics": max(0, total_topics_all - completed_topics_all),
        "total_study_hours": round(total_study_minutes / 60, 1),
        "total_study_minutes": total_study_minutes,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "courses": course_cards,
        "weekly_activity": weekly_data,
        "recent_activity": [
            {
                "id": a.id,
                "type": a.activity_type,
                "description": a.description,
                "time": a.created_at.strftime("%b %d, %I:%M %p") if a.created_at else ""
            }
            for a in recent_activities
        ]
    })
