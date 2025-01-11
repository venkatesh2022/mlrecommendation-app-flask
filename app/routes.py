from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
@routes_bp.route('/home')
def home():
    return render_template('home.html')

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('routes.home'))

@routes_bp.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'GET':
        # Provide a helpful message for GET requests
        return jsonify({'message': 'This endpoint requires a POST request with a user_id to provide recommendations.'})

    if request.method == 'POST':
        try:
            user_id = current_user.id  # Ensure the logged-in user's ID is used
            recommender = current_app.config['recommender']  # Access recommender from app context
            recommendations = recommender.recommend(user_id)
            return jsonify({'recommendations': recommendations})
        except Exception as e:
            return jsonify({'error': f'Error while generating recommendations: {str(e)}'})
