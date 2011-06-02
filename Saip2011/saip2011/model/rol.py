# -*- coding: utf-8 -*-
"""
Rol* related model.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession
from saip2011.model import *

__all__ = ['Rol']


# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
# esto se pone en la clase que va a usar los datos del otro

tabla_rol_privilegios = Table('TB_rol_privilegios', metadata,
	Column('idrol', Integer, ForeignKey('Tabla_Rol.idrol', onupdate="CASCADE", ondelete="CASCADE")),
	Column('idprivilegio', Integer, ForeignKey('Tabla_Privilegios.idprivilegio', onupdate="CASCADE", ondelete="CASCADE"))
)

class Rol(DeclarativeBase):
	"""
	Definicion del Rol    
	"""

        __tablename__ = 'Tabla_Rol'

	#{ Columns

	idrol = Column(Integer, autoincrement=True, primary_key=True)

	nombrerol = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column(Text)

	listaprivilegios = Column(Text)


	#{ Special methods

	def __repr__(self):
		return '<Rol: nombre=%s>' % self.nombrerol

	def __unicode__(self):
		return self.nombrerol
	
	#}
	@property
	def privilegios(self):
		"""Return a set of strings for the permissions granted."""
	    perms = set()
	    for g in self.roles:
	        perms = perms | set(g.privilegios)
	    return perms
