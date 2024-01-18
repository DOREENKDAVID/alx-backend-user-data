#!/usr/bin/env python3
"""session expiration module"""


from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from typing import Dict
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration date class."""
    user_id_by_session_id: Dict[str, Dict] = {}
    
    def __init__(self):
        """Initialize SessionExpAuth."""
        super().__init__()
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create a Session ID with expiration date."""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id]["session"] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return User ID based on Session ID with expiration date."""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id].get("session")
        if self.session_duration <= 0 or not session_dict or "created_at" not in session_dict:
            return None

        created_at = session_dict["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_dict["user_id"]
