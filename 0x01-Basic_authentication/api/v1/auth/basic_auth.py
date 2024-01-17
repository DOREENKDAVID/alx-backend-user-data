#!/usr/bin/env python3
"""Basic auth"""


from models.user import User
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64 part of Auth header for Basic Authentication."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the UTF-8 string of base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        padding = '=' * (4 - (len(base64_authorization_header) % 4) % 4)
        padded_base64 = base64_authorization_header + padding

        try:
            decoded_bytes = base64.b64decode(padded_base64)
            return decoded_bytes.decode('utf-8')
        except UnicodeDecodeError as e:
            return None
        except base64.binascii.Error as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and pwd from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        credentials = decoded_base64_authorization_header.split(':', 1)
        if len(credentials) != 2:
            return None, None

        user_email, user_password = credentials
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        if request is None:
            return None

        # Extract the base64 authorization header from the request
        base64_auth = self.authorization_header(request)

        # Decode the base64 authorization header
        decoded_auth = self.decode_base64_authorization_header(base64_auth)

        # Extract user credentials from the decoded header
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)

        # Retrieve the User instance based on email and password
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
