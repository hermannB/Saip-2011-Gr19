# -*- coding: utf-8 -*-
"""
Equipo de Desarrollo* related model.


"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession
from saip2011.model.item import Item , linea_base_item_tabla

__all__ = ['Linea_Base']


#{ Association tables



class Linea_Base (DeclarativeBase):
    """
   Definicion de Equipo de Desarrollo.
    
    """
    
    __tablename__ = 'Tabla_Linea_Base'
    
    #{ Columns
    
    id_linea_base = Column(Integer, autoincrement=True, primary_key=True)

    proyecto = Column(Integer, nullable=False)

    fase = Column(Integer, nullable=False)

    tipo =Column(Unicode(50),  nullable=False)          #parcial o general

    items = relation(Item, secondary=linea_base_item_tabla,
                      backref='lineas_bases')


   
   
    
    #{ Special methods
    
    def __repr__(self):
        return '<Tipo campos : id=%s>' % self.id_tipo_campos
    
    def __unicode__(self):
        return self.id_tipo_campos


    @classmethod
    def get_tipo_campos(self):
        """
        Obtiene la lista de todos los equipos
        registrados en el sistema
        """
        campos = DBSession.query(Tipo_Campos).all()
        return campos


    @classmethod
    def get_campos_by_tipo_item(self, id_tipo):
        campos = DBSession.query(Tipo_Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_tipo_item == int(4)):
                lista.append(campo)

        return lista
    #}

    @classmethod
    def get_nombres_by_tipo_item(self, id_tipo):
        campos = DBSession.query(Tipo_Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_tipo_item == id_tipo):
                lista.append(campo.nombre_campo)

        return lista
    #}

#
