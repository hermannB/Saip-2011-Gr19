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
	Column('id_rol', Integer, ForeignKey('Tabla_Rol.id_rol', onupdate="CASCADE", ondelete="CASCADE")),
	Column('id_privilegio', Integer, ForeignKey('Tabla_Privilegios.id_privilegio', onupdate="CASCADE", ondelete="CASCADE"))
)

class Rol(DeclarativeBase):
	"""
	Definicion del Rol    
	"""

        __tablename__ = 'Tabla_Rol'

	#{ Columns

	id_rol = Column(Integer, autoincrement=True, primary_key=True)

	nombre_rol = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column(Text)

	
	#{ Special methods

	def __repr__(self):
		return '<Rol: nombre=%s>' % self.nombre_rol

	def __unicode__(self):
		return self.nombre_rol
	
	#}
	@property
	def privilegios(self):
		"""Return a set of strings for the permissions granted."""
	    perms = set()
	    for g in self.roles:
	        perms = perms | set(g.privilegios)
	    return perms
