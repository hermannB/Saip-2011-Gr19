# -*- coding: utf-8 -*-
"""
Historial* related model.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Historial']



class Historial(DeclarativeBase):
	"""
	Group definition for :mod:`repoze.what`.

	Only the ``group_name`` column is required by :mod:`repoze.what`.

	"""

	__tablename__ = 'Tabla_Historial'

	#{ Columns

	idhistorial = Column(Integer, autoincrement=True, primary_key=True)

	iditem = Column(Integer, nullable=False)
	
	version = Column(Integer, nullable=False)

	creadopor = Column(Unicode(30), nullable=False)

	fechacreacion = Column(DateTime, default=datetime.now)
	
	descripcion = Column(Text)

	#{ Special methods

	def __repr__(self):
		return '<Historial: idHistorial=%s>' % self.idhistorial

	def __unicode__(self):
		return self.idhistorial
    
    #}


