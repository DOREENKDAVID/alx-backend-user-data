#!/usr/bin/env python3
"""
Session Auth views module
"""

from api.v1.auth.session_auth import SessionAuth
from api.v1.app import auth
from flask import Flask, jsonify, request, make_response
from models.user import User


app = Flask(__name__)


@app.route('/auth_session/login', methods=['POST', 'GET'], strict_slashes=False)
def login() -> str:
    """
    Handle Session authentication login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    user_json = user[0].to_json()
    
    response = make_response(jsonify(user_json))
    response.set_cookie(key=app.config['SESSION_NAME'], value=session_id)

    return response

@app_views.route('/auth_session/logout', methods=['DELETE', 'GET'], strict_slashes=False)
def logout() -> str:
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
