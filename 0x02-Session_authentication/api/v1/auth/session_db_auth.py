from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm.exc import NoResultFound


class SessionDBAuth(SessionExpAuth):
    """Session authentication with database storage class."""
    
    def create_session(self, user_id=None):
        """Create and store a new instance of UserSession."""
        session_id = super().create_session(user_id)
        if session_id:
            new_user_session = UserSession(user_id=user_id, session_id=session_id)
            new_user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return User ID by requesting UserSession in the database."""
        if session_id is None:
            return None

        try:
            user_session = UserSession.search({'session_id': session_id})
            return user_session.user_id if user_session else None
        except NoResultFound:
            return None

    def destroy_session(self, request=None):
        """Destroy UserSession based on the Session ID from the request cookie."""
        session_id = self.session_cookie(request)
        if session_id:
            try:
                user_session = UserSession.search({'session_id': session_id})
                user_session.remove()
                return True
            except NoResultFound:
                return False
        return False
