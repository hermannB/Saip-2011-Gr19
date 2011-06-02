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

	id_proyecto = Column(Integer, autoincrement=True, primary_key=True)

	nombre_proyecto = Column(Unicode(30), unique=True, nullable=False)

	id_equipo = Column(Integer, nullable=False)

	lista_Fases = Column(Text, nullable=False)	

	descripcion = Column(Text)	

	#{ Special methods

	def __repr__(self):
		return '<Proyecto: nombre=%s>' % self.nombre_proyecto

	def __unicode__(self):
		return self.nombre_proyecto

	@classmethod
	def get_proyectos(self):
		"""
		Obtiene la lista de todos los roles
		registrados en el sistema
		"""
		#Session = sessionmaker()
		#session = Session() 
		"""proyectos = session.query(cls).all()"""
		proyectos = DBSession.query(Proyecto).all()
		    
		return proyectos

	#}

