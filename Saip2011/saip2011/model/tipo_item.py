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

################################################################################

#               Tablas intermedias para relaciones Muchos a Muchos

#       Tabla Fase  -  Tipo Item

fase_tipo_item_tabla = Table('Tabla_Fase_Tipo_Item', metadata,
    Column('id_fase', Integer, ForeignKey('Tabla_Fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_tipo_item', Integer, ForeignKey('Tabla_Tipo_Item.id_tipo_item',
        onupdate="CASCADE", ondelete="CASCADE"))
)

#       Tabla  Tipo Fase  -  Tipo Item
tipo_fase_tipo_item_tabla = Table('Tabla_Tipo_Fase_Tipo_Item', metadata,
    Column('id_tipo_fase', Integer, ForeignKey('Tabla_Tipo_Fase.id_tipo_fase',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_tipo_item', Integer, ForeignKey('Tabla_Tipo_Item.id_tipo_item',
        onupdate="CASCADE", ondelete="CASCADE"))
)

################################################################################

class Tipo_Item(DeclarativeBase):
    """
    Definicion Tipo de Item

    """

    __tablename__ = 'Tabla_Tipo_Item'

################################################################################

    #           Columnas

    id_tipo_item = Column(Integer, autoincrement=True, primary_key=True)

    nombre_tipo_item = Column(Unicode(50), unique=True, nullable=False)

    codigo_tipo_item = Column(Unicode(50), nullable=False)

    descripcion = Column (Text)

################################################################################

    #               Metodos

    def __repr__(self):
        return '<Tipo Item: nombre=%s>' % self.nombre_tipo_item

    def __unicode__(self):
        return self.nombre_tipo_item

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipos_items(self):
        """
        Obtiene la lista de todos los tipos de item
        registrados en el sistema
        """
        tipos_items = DBSession.query(Tipo_Item).all()
        return tipos_items

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_item_by_id(self,tipo_item_id):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        tipo_items = DBSession.query(Tipo_Item).all()
        for tipo_item in tipo_items:
            if tipo_item.id_tipo_item == tipo_item_id:
                return tipo_item

#-------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------

    @classmethod
    def get_campos_by_tipo(self, id_tipo):
        """
        Obtiene la lista de todos los tipos de item
        registrados en el sistema
        """
        lista=Tipo_Campos.get_campos_by_tipo_item(id_tipo)
        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombres_campos_by_tipo(self, id_tipo):
        """
        Obtiene la lista de todos los tipos de item
        registrados en el sistema
        """
        lista=Tipo_Campos.get_nombres_by_tipo_item(id_tipo)
        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_tipo_item):
        """
        Obtiene la lista de todos los tipo_item         
        """
        DBSession.delete(DBSession.query(Tipo_Item).get(id_tipo_item))
        DBSession.flush()	

#-------------------------------------------------------------------------------
################################################################################

