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
from saip2011.model.tipo_item import Tipo_Item
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

	codigo_item = Column(Unicode(50), nullable=False)		

	id_tipo_item = Column(Integer, ForeignKey('Tabla_Tipo_Item.id_tipo_item'))

	nombre_tipo_item = relation('Tipo_Item', backref='Item')

	fase = Column(Unicode(50), nullable=False)

	proyecto = Column(Unicode(50), nullable=False)

	complejidad = Column(Integer, nullable=False)

	estado = Column(Unicode(50), nullable=False)

	estado_oculto = Column(Unicode(50), nullable=False)

	version = Column(Integer)

	creado_por = Column(Unicode(50), nullable=False)

	fecha_creacion = Column(DateTime, default=datetime.now)

	#{ Special methods

	def __repr__(self):
		return '<Item: Id Item=%s>' % self.id_item

	def __unicode__(self):
		return self.id_item

	@classmethod
	def get_ultimo_id(self):
		"""
		Obtiene el ultimo id de la tabla
		"""
		mayor =0
		items = DBSession.query(Item).all()
		for item in items:
			if (item.id_item > mayor):
				mayor =item.id_item

		return mayor

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
	def crear_codigo(self,id_tipo):
		"""
		crear el codigo del item
		"""
		codigo=""
		cantidad=1
		tipo = DBSession.query(Tipo_Item).get(id_tipo)
		items = DBSession.query(Item).all()

		palabras =tipo.nombre_tipo_item.split(" ")
		for p in palabras:
			codigo+=p[0].upper()
		codigo+="-"

		for i in items:
			if (i.id_tipo_item == id_tipo):
				cantidad=cantidad+1
		codigo+=str(cantidad)
		return codigo

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
			if( (item.proyecto == muestra.proyecto)  and (item.fase == muestra.fase ) 
					and ( item.codigo_item ==muestra.codigo_item) and (item.estado_oculto == "Desactivado") ):
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


