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

__all__ = ['Privilegios']


class Privilegios(DeclarativeBase):
	"""
	Definicion de los privilegios    
	"""

	__tablename__ = 'Tabla_Privilegios'

	#{ Columns

	idprivilegios = Column(Integer, autoincrement=True, primary_key=True)

	nombreprivilegio = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column (Text)


	#{ Special methods

	def __repr__(self):
		return '<Privilegio: nombre=%s>' % self.nombreprivilegio

	def __unicode__(self):
		return self.nombreprivilegio
	#}


