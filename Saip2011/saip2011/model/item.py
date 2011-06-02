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

	id_tipo_item = Column(Integer, ForeignKey('Tabla_Tipo_Item.id_tipo_item'))

  	nombre_tipo_item = relation('Tipo_Item', backref='Item')

	fase = Column(Unicode(50), nullable=False)

	proyecto = Column(Unicode(50), nullable=False)

	adjunto = Column(Integer)

	complejidad = Column(Integer, nullable=False)

	estado = Column(Unicode(50), nullable=False)

	estado_oculto = Column(Unicode(50), nullable=False)

	#campos = Column(Text, nullable=False)

	#lista_item = Column(Text)

	version = Column(Integer)

	creado_por = Column(Unicode(50), nullable=False)

	fecha_creacion = Column(DateTime, default=datetime.now)
	
	#{ Special methods

	def __repr__(self):
		return '<Item: Id Item=%s>' % self.id_item

	def __unicode__(self):
		return self.id_item
	@classmethod
        def get_item_activados(self):
		"""
		Obtiene la lista de todos los items
		registrados en el sistema
		"""
		lista=[]
		items = DBSession.query(Item).all()
		for item in items:
		  if( item.estado_oculto=="Activo"):
		     lista.append(item)  
		return lista

	@classmethod
        def get_item_eliminados(self):
		"""
		Obtiene la lista de todos los items
		registrados en el sistema
		"""
		lista=[]
		items = DBSession.query(Item).all()
		for item in items:
		  if( item.estado_oculto=="Eliminado"):
		     lista.append(item)  
		return lista


	@classmethod
        def get_historial(self, id_item):
		"""
		Obtiene la lista de todos los items
		registrados en el sistema
		"""
		muestra=DBSession.query(Item).get(id_item)
		lista=[]
		items = DBSession.query(Item).all()
		for item in items:
		  if( (item.nombre_item == muestra.nombre_item) and  (item.proyecto == muestra.proyecto)  and (item.fase == muestra.fase ) ):
		     lista.append(item)  
		return lista

	@classmethod
        def version_actual(self, id_item):
		"""
		Obtiene la lista de todos los items
		registrados en el sistema
		"""
		
		items = Item.get_item_activados()
		item_viejo = DBSession.query(Item).get(id_item)
		for item in items:
		  if( (item.nombre_item == item_viejo.nombre_item) and  (item.proyecto == item_viejo.proyecto)  and (item.fase == item_viejo.fase ) ):
		     return item 
		 

	#}


