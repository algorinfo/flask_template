import flask_login
from changeme.db.sql import SQL
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
# from web import login as login_manager
from werkzeug.security import check_password_hash, generate_password_hash


class User(flask_login.UserMixin, SQL.Base):
    """ Default User model """

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    _password = Column("password", String, nullable=False)

    @hybrid_property
    def password(self):
        """Used as setter and getter """
        return self._password

    @password.setter
    def password(self, uncrypted):
        """ Generates a hash from a uncrypted passwoerd"""
        hashed = generate_password_hash(uncrypted)
        self._password = hashed

    def check_password(self, uncrypted):
        return check_password_hash(self._password, uncrypted)

    def get_id(self):
        """
        Needed by flask-login
        """
        return self.id


# @login_manager.user_loader
# def user_loader(username):
#
#    u = User.query.get(username)
#    return u
#
#
# @login_manager.request_loader
# def request_loader(request) -> :
#    _u = request.form.get('username')
#    user = User.query.get(_u)
#    if user is not None:
#        if request.form['password'] == user.password_hash:
#            user.is_authenticated = True
#            return user
#    else:
#        return
