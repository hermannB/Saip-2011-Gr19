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

	id_historial = Column(Integer, autoincrement=True, primary_key=True)

	id_item = Column(Integer, nullable=False)
	
	version = Column(Integer, nullable=False)

	creado_por = Column(Unicode(50), nullable=False)

	fecha_creacion = Column(DateTime, default=datetime.now)
	
	descripcion = Column(Text)

	#{ Special methods

	def __repr__(self):
		return '<Historial: id_Historial=%s>' % self.id_historial

	def __unicode__(self):
		return self.id_historial

        @classmethod
        def get_historiales(self):
		"""
		Obtiene la lista de todos los historiales
		registrados en el sistema
		"""

		historiales = DBSession.query(Historial).all()
		    
		return historiales

    
    #}


