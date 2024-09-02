from flask import request, jsonify, current_app
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
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing username, email, or password"}), 400

    try:
        # Create the user in Firebase
        user = auth.create_user(email=email, password=password)
        custom_token = auth.create_custom_token(user.uid)

        # Access the MongoDB database from the app config
        db = current_app.config['db']
        users_collection = db['users']

        # Store the username and email in MongoDB
        user_data = {
            "username": username,
            "email": email,
            "firebase_uid": user.uid
        }
        users_collection.insert_one(user_data)

        return jsonify({"token": custom_token.decode('utf-8')}), 201
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 400


# Endpoint  getch user info from Mongo DB
@auth_bp.route('/user-info', methods=['GET'])
def get_user_info():
    email = request.args.get('email')  # Get the email from query parameters

    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    try:
        db = current_app.config['db']
        users_collection = db['users']
        user = users_collection.find_one({"email": email}, {'_id': 0})  # Fetch user by email, exclude the MongoDB ObjectID

        if user:
            return jsonify({"user": user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500