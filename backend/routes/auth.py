from flask import Blueprint, request, jsonify
from models import Admin
from extensions import db
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from utils.token import generate_reset_token
from utils.token import verify_reset_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")




@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    if current_user.is_authenticated:
        return {
            "authenticated": True,
            "user": {
                "id": current_user.id,
                "name": current_user.full_name,
                "email": current_user.email
            }
        }
    return {"authenticated": False}


# 🔐 SIGNUP
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    full_name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not full_name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    # Check if user exists
    existing_user = Admin.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    # Create user
    user = Admin(full_name=full_name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201


# 🔐 LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = Admin.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(user)

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email
        }
    })


# 🔐 LOGOUT
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = Admin.query.filter_by(email=email).first()

    # 🔥 Always return success (security)
    if user:
        token = generate_reset_token(email)

        reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

        print("\n🔐 PASSWORD RESET LINK:")
        print(reset_link)
        print("\n")

    return jsonify({"message": "If the email exists, a reset link has been sent"})

@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json()
    new_password = data.get("password")

    email = verify_reset_token(token)

    if not email:
        return jsonify({"error": "Invalid or expired token"}), 400

    user = Admin.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password reset successful"})