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

__all__ = ['Rol']


class Rol(DeclarativeBase):
	"""
	Definicion del Rol    
	"""

	__tablename__ = 'Tabla_Rol'

	#{ Columns

	idrol = Column(Integer, autoincrement=True, primary_key=True)

	nombrerol = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column(Text)

	listaprivilegios = Column (Text)


	#{ Special methods

	def __repr__(self):
		return '<Rol: nombre=%s>' % self.nombrerol

	def __unicode__(self):
		return self.nombrerol
	
	#}

