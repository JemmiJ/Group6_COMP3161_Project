from functools import wraps
from flask import request, jsonify
from functools import wraps
from flask import session, redirect, url_for, flash
from flask_login import current_user
import jwt
import os

secret = os.environ.get('SECRET_KEY')

def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, secret, algorithms=["HS256"])
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('app_views.login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator