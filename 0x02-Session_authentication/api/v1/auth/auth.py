#!/usr/bin/env python3

"""API authentication module"""


from flask import request
from typing import List, TypeVar
import os

class Auth:
    """API authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ return path and excluded path
        returns True if the path is not in the list of strings excluded_paths.
        - Returns True if path is None.
        - Returns True if excluded_paths is None or empty.
        - Returns False if path is in excluded_paths.

        Assumes excluded_paths contain string paths always ending with a /
        """
        if path is None:
            return True
        elif excluded_paths is None or not excluded_paths:
            return True

        n_path = path.rstrip("/")
        for excluded_path in excluded_paths:
            n_excluded = excluded_path.rstrip("/")
            if n_excluded.endswith('*') and n_path.startswith(n_excluded[:-1]):
                return False
            elif n_path == n_excluded:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization headers
        If request is None, returns None.
        If request doesn’t contain the header key Authorization, returns None.
        return the value of the header request Authorization."""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """return current user"""
        return None


    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(cookie_name, None)
