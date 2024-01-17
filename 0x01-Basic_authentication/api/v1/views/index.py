#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, Blueprint
from api.v1.views import app_views


app_views = Blueprint('app_views', __name__)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/api/v1/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized_endpoint():
    """raise 401 error with abort"""
    abort(401)
    return jsonify({"error": "Unauthorized"})


@app_views.route('/api/v1/forbidden', methods=['GET'], strict_slashes=False)
def forbidden():
    """raise forbidden error on abort"""
    abort(403)
    return jsonify({"error": "Forbidden"})


@app_views.route('/api/v1/users', methods=['GET'])
def get_users():
    """route for users endpoint"""
    # Get the authenticated user for the current request
    authenticated_user = auth.current_user(request)

    if authenticated_user is None:
        # If there is no authenticated user, return an unauthorized error
        abort(401)

    # Return information about the authenticated user
    user_info = {
        "email": authenticated_user.email,
        "username": authenticated_user.username,
    }
