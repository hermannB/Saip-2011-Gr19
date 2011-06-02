# -*- coding: utf-8 -*-
"""
Fase* related model.


It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text , String
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Tipo_Fase']


class Tipo_Fase(DeclarativeBase):
	"""
	Definicion de Fase.

	"""

	__tablename__ = 'Tabla_Tipo_Fase'

	#{ Columns

	id_tipo_fase = Column(Integer, autoincrement=True, primary_key=True)

	nombre_tipo_fase = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column(Text)
	
	#{ Special methods

	def __repr__(self):
		return '<Fase: Nombre=%s>' % self.nombre_tipo_fase
	
	def __unicode__(self):
		return self.nombre_tipo_fase

	@classmethod
	def get_tipo_fase(self):
		"""
		Obtiene la lista de todos los roles
		registrados en el sistema
		"""
		#Session = sessionmaker()
		#session = Session() 
		"""tiposfases = session.query(cls).all()"""
		tipos_fases = DBSession.query(Tipo_Fase).all()
		    
		return tipos_fases

	#}

