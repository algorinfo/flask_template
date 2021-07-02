import logging
from contextlib import contextmanager
from typing import Optional

from flask import _app_ctx_stack
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class SQL:
    """
    Manage sql connections using sqlalchemy
    It could be used in the context of a flask app or standalone
    """

    Base = declarative_base()

    def __init__(self, sqluri=None):
        self._uri = sqluri
        if sqluri:
            self._engine = create_engine(sqluri)
        else:
            self._engine = None

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

    def create_conn(self, autocommit=False, autoflush=False) -> sessionmaker:
        if not self._engine:
            self._engine = create_engine(self._uri)

        return sessionmaker(autocommit=autocommit,
                            autoflush=autoflush,
                            bind=self._engine)

    def create_db(self):
        """ This will create the database with their tables if not exist
        """
        self.Base.metadata.create_all(bind=self._engine)

    @contextmanager
    def session_local(self):
        """ Create a session but is not a scoped session,
        So is not thread aware. This could be used when
        multiple connections don't will be needed
        See https://docs.sqlalchemy.org/en/14/orm/contextual.html
        For more information.
        """
        SessionMaker = self.create_conn()
        local = SessionMaker()
        try:
            yield local
        finally:
            local.remove()

    @contextmanager
    def session_scope(self):
        session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self._engine))
        try:
            yield session
        finally:
            session.remove()

    def get_session(self, autoflush=False, autocommit=False) -> Session:
        """ Simple get_session for flask context 
        Some logic should exist to close and remove the session."""
        # SessionLocal = self.create_conn(self._uri)
        session = scoped_session(
            sessionmaker(autocommit=autocommit, autoflush=autoflush,
                         bind=self._engine))

        return session

    def init_app(self, app):
        """ Used by flask 
        Initialize and load this object on FLASK
        """
        self._engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

        # self.setup_connection(app.config['SQLALCHEMY_DATABASE_URI'])
        # app.extensions[self._PLUGIN] = self

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        """
        Closes the sqlalchemy session when a request ends.
        """
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "sql_session"):
            ctx.sql_session.rollback()
            ctx.sql_session.remove()
            self.logger.debug("SQL session removed")

    @property
    def flask(self) -> Optional[Session]:
        """ db session to be used in the context of a flask app"""
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "sql_session"):
                ctx.sql_session = self.get_session()
            return ctx.sql_session

    def drop_all(self):
        self.Base.metadata.drop_all(bind=self._engine)


def commit(session):
    """
    Commit session, if fail then will make a rollback.

    :return: bool
    """
    ok = True
    try:
        session.commit()
    except exc.InternalError as i:
        session.rollback()
        logging.error(i)
        ok = False

    return ok


class MutableList(Mutable, list):
    """ This allow modify an ARRAY custom type
    From https://gist.github.com/kirang89/22d111737af0fca251e3

    """

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        list.__delitem__(self, key)
        self.changed()

    def append(self, value):
        list.append(self, value)
        self.changed()

    def pop(self, index=0):
        value = list.pop(self, index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value
