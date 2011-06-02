# -*- coding: utf-8 -*-
"""
Proyecto * related model.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Proyecto']

class Proyecto(DeclarativeBase):
	"""

	Definicion del ṕroyecto

	"""

	__tablename__ = 'Tabla_Proyecto'

	#{ Columns

	idproyecto = Column(Integer, autoincrement=True, primary_key=True)

	nombreproyecto = Column(Unicode(30), unique=True, nullable=False)

	idequipo = Column(Integer, nullable=False)

	listaFases = Column(Text, nullable=False)	

	descripcion = Column(Text)	

	#{ Special methods

	def __repr__(self):
		return '<Proyecto: nombre=%s>' % self.nombreproyecto

	def __unicode__(self):
		return self.nombreproyecto

	#}

