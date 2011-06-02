# -*- coding: utf-8 -*-
"""
Auth* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip2011 application,
though.

"""

import os
from datetime import datetime
import transaction
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Usuario', 'Rol', 'Privilegios']


#{ Association tables


# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
rol_privilegio_tabla = Table('Tabla_Rol_Privilegios', metadata,
    Column('rol_id', Integer, ForeignKey('Tabla_Rol.idrol',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('privilegio_id', Integer, ForeignKey('Tabla_Privilegios.idprivilegio',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships. It's required by repoze.what.
usuario_rol_tabla = Table('Tabla_Usuario_Rol', metadata,
    Column('usuario_id', Integer, ForeignKey('Tabla_Usuario.idusuario',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('rol_id', Integer, ForeignKey('Tabla_Rol.idrol',
        onupdate="CASCADE", ondelete="CASCADE"))
)


#{ The auth* model itself


class Rol(DeclarativeBase):
    """
    Group definition for :mod:`repoze.what`.
    
    Only the ``group_name`` column is required by :mod:`repoze.what`.
    
    """
    
    __tablename__ = 'Tabla_Rol'
    
    #{ Columns
    
    idrol = Column(Integer, autoincrement=True, primary_key=True)
    
    nombrerol = Column(Unicode(50), unique=True, nullable=False)

    descripcion = Column(Text)

    
	#{ Special methods

   

    def __repr__(self):
        return '<Rol: nombre=%s>' % self.nombrerol

    def __unicode__(self):
        return self.nombrerol
    
    @classmethod
    def get_roles(self):
        """
        Obtiene la lista de todos los roles
        registrados en el sistema
        """
        #Session = sessionmaker()
        #session = Session() 
        """roles = session.query(cls).all()"""
        roles = DBSession.query(Rol).all()
            
        return roles

    #{ Relations
    
    usuarios = relation('Usuario', secondary=usuario_rol_tabla, backref='roles')
    
        
    #}


# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.
class Usuario(DeclarativeBase):
    """
    User definition.
    
    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.
    
    """
    __tablename__ = 'Tabla_Usuario'
    
    #{ Columns

    idusuario = Column(Integer, autoincrement=True, primary_key=True)
    
    alias = Column(Unicode(50), unique=True, nullable=False)
    nombre = Column(Unicode(50), nullable=False)
    apellido = Column(Unicode(50), nullable=False)
    _password = Column('password', Unicode(80),info={'rum': {'field':'Password'}})

    rol = Column(Unicode(50))
    email_address = Column(Unicode(50), unique=True, nullable=False, info={'rum': {'field':'Email'}})

    nacionalidad = Column(Unicode(50))
    tipodocumento = Column(Unicode(50), nullable=True)
    nrodoc = Column(Integer, unique=True, nullable=True)

    
    #{ Special methods

    def __repr__(self):
	return '<User: email="%s", Alias="%s">' % (self.email_address, self.alias)

    def __unicode__(self):
        return self.alias
    
    #{ Getters and setters

    @property
    def privilegios(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.roles:
            perms = perms | set(g.privilegios)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter(cls.email_address==email).first()

    @classmethod
    def by_alias(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter(cls.alias==username).first()

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        hashed_password = password
        
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        # Make sure the hashed password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode
        # columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))
    
    #}
    
    def validate_password(self, password):
        """
        Check the password against existing credentials.
        
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()

    @classmethod
    def get_usuarios(self):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        #Session = sessionmaker()
        #session = Session() 
        """usuarios = session.query(cls).all()"""
        usuarios = DBSession.query(Usuario).all()
            
        return usuarios

    @classmethod
    def get_user_by_id(self, iduser):
        """
        Obtiene el usuario por su id
        """
        usuario, = DBSession.query(Usuario).filter_by(idusuario=iduser)
        
        return usuario

class Privilegios(DeclarativeBase):
    """
    Permission definition for :mod:`repoze.what`.
    
    Only the ``permission_name`` column is required by :mod:`repoze.what`.
    
    """
    
    __tablename__ = 'Tabla_Privilegios'
    
    #{ Columns

    idprivilegio = Column(Integer, autoincrement=True, primary_key=True)
    
    nombreprivilegio = Column(Unicode(50), unique=True, nullable=False)

    descripcion = Column(Text)
    
    #{ Relations
    
    roles = relation(Rol, secondary=rol_privilegio_tabla,
                      backref='privilegios')
    
    #{ Special methods
    
    def __repr__(self):
        return '<Privilegio: nombre=%s>' % self.nombreprivilegio

    def __unicode__(self):
        return self.nombreprivilegio
    
    @classmethod
    def get_privilegio(self):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        #Session = sessionmaker()
        #session = Session() 
        """privilegios = session.query(cls).all()"""
        privilegios = DBSession.query(Privilegios).all()
            
        return privilegios

    #}


#}
