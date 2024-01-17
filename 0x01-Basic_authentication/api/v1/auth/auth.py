#!/usr/bin/env python3
"""API authentication module"""


from flask import request
from typing import List, TypeVar


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
            if n_path == n_excluded:
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
