from flask import Blueprint, redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Skill, Goal

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('routes.dashboard'))
    else:
        return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password.")
    else:
        return render_template('login.html')

@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes.route('/dashboard')
def dashboard():
    user_id = current_user.id
    user = User.query.get(user_id)
    skills = Skill.query.filter_by(user_id=user_id).all()
    goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user, skills=skills, goals=goals)

@routes.route('/add_skill', methods=['POST'])
def add_skill():
    if request.method == 'POST':
        skill_name = request.form.get('skill_name')
        hours_logged_str = request.form.get('hours_logged')
        goal_details = request.form.get('goal_details')

        if hours_logged_str is None:
            return redirect(url_for('routes.dashboard'))

        try:
            hours_logged = int(hours_logged_str)
        except ValueError:
            return redirect(url_for('routes.dashboard'))

        existing_skill = Skill.query.filter_by(name=skill_name, user_id=current_user.id).first()

        if existing_skill:
            existing_skill.hours_logged += hours_logged
            existing_skill.goal_details = goal_details
        else:
            new_skill = Skill(name=skill_name, hours_logged=hours_logged, goal_details=goal_details, user_id=current_user.id)
            db.session.add(new_skill)
        
        db.session.commit()

        return redirect(url_for('routes.dashboard'))

@routes.route('/skill/<int:skill_id>')
def skill_detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    goal_details = [skill.goal_details] if skill.goal_details else []
    return render_template('skill_detail.html', skill=skill, goal_details=goal_details)

@routes.route('/delete_skill/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user != current_user:
        abort(403)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill has been deleted!', 'success')
    return redirect(url_for('routes.dashboard'))
