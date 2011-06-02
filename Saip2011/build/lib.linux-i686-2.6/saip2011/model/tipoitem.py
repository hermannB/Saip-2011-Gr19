# -*- coding: utf-8 -*-
"""
Tipo Item* related model.


"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['TipoItem']


class TipoItem(DeclarativeBase):
	"""
	Definicion Tipo de Item

	"""

	__tablename__ = 'Tabla_TipoItem'

	#{ Columns

	idtipo = Column(Integer, autoincrement=True, primary_key=True)

	nombretipo = Column(Unicode(30), unique=True, nullable=False, index=True)

	descripcion = Column (Text)
	
	#{ Special methods

	def __repr__(self):
		return '<Tipo Item: nombre=%s>' % self.nombretipo

	def __unicode__(self):
		return self.nombretipo

	#}


