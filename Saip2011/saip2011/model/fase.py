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

__all__ = ['Fase']


class Fase(DeclarativeBase):
	"""
	Definicion de Fase.

	"""

	__tablename__ = 'Tabla_Fase'

	#{ Columns

	id_fase = Column(Integer, autoincrement=True, primary_key=True)

	nombre_fase = Column(Unicode(50), unique=True, nullable=False)

   	id_tipo_fase = Column(Integer, ForeignKey('Tabla_Tipo_Fase.id_tipo_fase'))

  	nombre_tipo_fase = relation('Tipo_Fase', backref='Fase')

	estado = Column(Unicode(50), nullable=False)

	linea_base =Column (Unicode(50), nullable=False)
	
	descripcion = Column(Text)
	
	#{ Special methods

	def __repr__(self):
		return '<Fase: Nombre=%s>' % self.nombre_fase
	
	def __unicode__(self):
		return self.nombre_fase
       
        @classmethod
        def get_fase(self):
		"""
		Obtiene la lista de todos los usuarios
		registrados en el sistema
		"""

		fases = DBSession.query(Fase).all()
		    
		return fases

	

	#}

