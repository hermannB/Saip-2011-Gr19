# -*- coding: utf-8 -*-
"""
Usuario* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession
from saip2011.model.equipodesarrollo import EquipoDesarrollo , tabla_equipo_usuario

__all__ = ['Usuario']


# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.
class Usuario(DeclarativeBase):
	"""
	Definicion usuario.

	This is the user definition used by :mod:`repoze.who`, which requires at
	least the ``alias`` column.

	"""
	__tablename__ = 'Tabla_Usuario'

	#{ Columns

	id_usuario = Column(Integer, autoincrement=True, primary_key=True)

	alias = Column(Unicode(30), unique=True, nullable=False)

	nombre = Column(Unicode(30), nullable=False)

	apellido = Column(Unicode(30), nullable=False)

	password = Column('Password', Unicode(80),info={'rum': {'field':'Password'}})

	email_address = Column(Unicode(80), unique=True, nullable=False, info={'rum': {'field':'Email'}})

	nacionalidad = Column(Unicode(30))

	tipodocumento = Column(Unicode(30))

	nrodoc = Column(Integer, unique=True)


	 #{ Relacio usuario equipo
    
	miembrousuario = relation(EquipoDesarrollo, secondary=tabla_equipo_usuario, backref='Alias')
    

	#{ Special methods

	def __repr__(self):
		return '<User: email="%s", Alias="%s">' % (self.email_address, self.alias)

	def __unicode__(self):
        	return self.alias
    
    #{ Getters and setters

#    @property
#    def permissions(self):
#        """Return a set of strings for the permissions granted."""
#        perms = set()
#        for g in self.groups:
#            perms = perms | set(g.permissions)
#        return perms

	@classmethod
	def by_email_address(cls, email):
		"""Return the user object whose email address is ``email``."""
		return DBSession.query(cls).filter(cls.email_address==email).first()

	@classmethod
	def by_alias(cls, apodo):
		"""Return the user object whose user name is ``alias``."""
	        return DBSession.query(cls).filter(cls.alias==apodo).first()

	
