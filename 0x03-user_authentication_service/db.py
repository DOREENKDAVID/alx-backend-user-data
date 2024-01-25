#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """The method should save the user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ method takes in arbitrary keyword arguments and
        returns the first row found in the users table
        as filtered by the method’s input arguments.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("Not found")
            return user
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid")

    def update_user(self, user_id: int, **kwargs) -> None:
        """to locate the user to update, then will update the user’s
        attributes as passed in the method’s
        arguments then commit changes to the database"""
        try:
            # Find the user by user_id
            user = self.find_user_by(id=user_id)

            # Update the user's attributes
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError("Error")

            # Commit changes to the database
            self._session.commit()

        except NoResultFound as e:
            raise NoResultFound("Not found")
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid")
