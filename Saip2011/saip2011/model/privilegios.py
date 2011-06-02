# -*- coding: utf-8 -*-
"""
Privilefios * related model.


"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

from saip2011.model.rol import Rol , tabla_rol_privilegios

__all__ = ['Privilegio' ]


class Privilegio(DeclarativeBase):
	"""
	Definicion de los privilegios    
	"""

	__tablename__ = 'Tabla_Privilegios'

	#{ Columns

	id_privilegio = Column(Integer, autoincrement=True, primary_key=True)

	nombre_privilegio = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column (Text)

	 #{ Relations   /// se indica quien me va a usar
    
	roles = relation(Rol, secondary=tabla_rol_privilegios, backref='Privilegios')

	#{ Special methods

	def __repr__(self):
		return '<Privilegio: nombre=%s>' % self.nombre_privilegio

	def __unicode__(self):
		return self.nombre_privilegio
	


	#}



