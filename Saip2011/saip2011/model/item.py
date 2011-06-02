# -*- coding: utf-8 -*-
"""
Auth* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Item']




class Item(DeclarativeBase):
	"""
	Definicion Item
	"""

	__tablename__ = 'Tabla_Item'

	#{ Columns

	id_item = Column(Integer, autoincrement=True, primary_key=True)

	nombre_item = Column(Unicode(50), nullable=False)	

	tipo_item = Column(Unicode(50), nullable=False)

	fase = Column(Unicode(50), nullable=False)

	proyecto = Column(Unicode(50), nullable=False)

	adjunto = Column(Integer)

	complejidad = Column(Integer, nullable=False)

	estado = Column(Unicode(50), nullable=False)

	campos = Column(Text, nullable=False)

	lista_item = Column(Text)

	creado_por = Column(Unicode(50), nullable=False)

	fecha_creacion = Column(DateTime, default=datetime.now)
	
	#{ Special methods

	def __repr__(self):
		return '<Item: Id Item=%s>' % self.id_item

	def __unicode__(self):
		return self.id_item
	@classmethod
        def get_item(self):
		"""
		Obtiene la lista de todos los items
		registrados en el sistema
		"""

		items = DBSession.query(Item).all()
		    
		return items

	#}


