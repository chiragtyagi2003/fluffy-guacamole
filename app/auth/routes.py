from flask import request, jsonify
from firebase_admin import auth
from app.auth import auth_bp

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return jsonify({"token": custom_token.decode('utf-8')}), 200
    except Exception as e:
        return f"Login failed: {str(e)}", 400

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.create_user(email=email, password=password)
        custom_token = auth.create_custom_token(user.uid)
        return jsonify({"token": custom_token.decode('utf-8')}), 201
    except Exception as e:
        return f"Registration failed: {str(e)}", 400
