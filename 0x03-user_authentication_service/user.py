#!/usr/bin/env python3
"""user authentification module"""


import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """user log in details stored in the db so the user can remain logged
    on remeber me functionaity"""

    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(250), unique=True,
                                             nullable=False)
    hashed_password: so.Mapped[str] = so.mapped_column(sa.String(250),
                                                       nullable=False)
    session_id: so.Mapped[str] = so.mapped_column(sa.String(250),
                                                  nullable=True)
    reset_token: so.Mapped[str] = so.mapped_column(sa.String(250),
                                                   nullable=True)

    def __repr__(self):
        """
        String rep.
        """
        return f"User: id={self.id}"
