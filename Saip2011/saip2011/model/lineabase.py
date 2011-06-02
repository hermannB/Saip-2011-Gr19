# -*- coding: utf-8 -*-
"""
Linea Base* related model.


"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['LineaBase']


#{ The Linea Base* model itself


class LineaBase(DeclarativeBase):
	"""
	Definicion de Linea Base

	"""

	__tablename__ = 'Tabla_LineaBase'

	#{ Columns

	idlineabase = Column(Integer, autoincrement=True, primary_key=True)

	estado = Column(Unicode(30), nullable=False)

	fechacreacion = Column(DateTime, default=datetime.now)

	#{ Special methods

	def __repr__(self):
		return '<Linea Base: estado=%s>' % self.estado

	def __unicode__(self):
		return self.estado

	#}

