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
from saip2011.model.tipo_campos import Tipo_Campos


__all__ = ['Tipo_Item']


class Tipo_Item(DeclarativeBase):
	"""
	Definicion Tipo de Item

	"""

	__tablename__ = 'Tabla_Tipo_Item'

	#{ Columns

	id_tipo_item = Column(Integer, autoincrement=True, primary_key=True)

	nombre_tipo_item = Column(Unicode(50), unique=True, nullable=False)

	descripcion = Column (Text)
	
	#{ Special methods

	def __repr__(self):
		return '<Tipo Item: nombre=%s>' % self.nombre_tipo_item

	def __unicode__(self):
		return self.nombre_tipo_item

	@classmethod
	def get_tipo_item(self):
		"""
		Obtiene la lista de todos los tipos de item
		registrados en el sistema
		"""

		tipos_items = DBSession.query(Tipo_Item).all()
		    
		return tipos_items

	@classmethod
	def get_ultimo_id(self):
		"""
		Obtiene el ultimo id de la tabla
		"""
		mayor =0
		tipos_items = DBSession.query(Tipo_Item).all()
		for tipo_item in tipos_items:
		   if (tipo_item.id_tipo_item > mayor):
		      mayor =tipo_item.id_tipo_item

		return mayor

	@classmethod
	def get_campos(self, id_tipo):
		"""
		Obtiene la lista de todos los tipos de item
		registrados en el sistema
		"""
		lista=Tipo_Campos.get_nombres_by_tipo_item(id_tipo)

		    
		return lista


	#}


