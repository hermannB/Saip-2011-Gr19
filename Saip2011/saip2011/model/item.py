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
from saip2011.model.variables import Variables
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
    def get_item_proy_fase(self,proy,fase):
        """
        Obtiene la lista de todos los items
        registrados en el sistema
        """
        lista=[]
        items = DBSession.query(Item).all()
        for item in items:
	        if( item.estado_oculto=="Activo" and item.proyecto == proy
                and item.fase == fase):
		        lista.append(item)  
        return lista

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
    def get_item_activados_by_fase(self,fase):
        """
        Obtiene la lista de todos los items
        registrados en el sistema
        """
        proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        lista=[]
        items = DBSession.query(Item).all()
        for item in items:
            if( item.estado_oculto=="Activo" and item.proyecto == proyecto
                and item.fase == fase):
                lista.append(item)  
        return lista

	@classmethod
	def crear_codigo(self,id_tipo,pre_codigo,proy_actual,fas_act):
		"""
		crear el codigo del item
		"""
		codigo=""
		cantidad=1
		tipo = DBSession.query(Tipo_Item).get(id_tipo)
		items = DBSession.query(Item).all()

		codigo+=pre_codigo+"-"

		for i in items:
			if (i.id_tipo_item == id_tipo and i.proyecto == proy_actual
                and i.fase == fas_act):
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
    def get_item_eliminados_by_fase(self,fase):
        """
        Obtiene la lista de todos los items
        registrados en el sistema
        """
        proyecto=int(Variables.get_valor_by_nombre("proyecto_actual"))
        lista=[]
        items = DBSession.query(Item).all()
        for item in items:
	        if( item.estado_oculto=="Eliminado"and item.proyecto == proyecto
                and item.fase == fase):
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
		 
	@classmethod
	def activar(self, id_item):
		item = DBSession.query(Item).get(id_item)
		if item.estado == "nuevo":
			item.estado="en_desarrollo"
			DBSession.flush()

	@classmethod
	def aprobar(self, id_item):
		item = DBSession.query(Item).get(id_item)
		if item.estado == "en_desarrollo":
			item.estado="aprobado"
			DBSession.flush()

	@classmethod
	def con_linea_base(self, id_item):
		item = DBSession.query(Item).get(id_item)
		if item.estado == "aprobado":
			item.estado="con_linea_base"
			DBSession.flush()

	@classmethod
	def revisar(self, id_item):
		item = DBSession.query(Item).get(id_item)
		if item.estado == "aprobado" or item.estado == "con_linea_base":
			item.estado="a_revisar"
			DBSession.flush()

	@classmethod
	def finalizar(self, id_proyecto):
		proyecto = DBSession.query(Proyecto).get(id_proyecto)
		if item.estado == "con_linea_base":
			proyecto.estado="finalizado"
			DBSession.flush()

    #}


