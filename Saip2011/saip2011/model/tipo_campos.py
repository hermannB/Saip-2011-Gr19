6# -*- coding: utf-8 -*-
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

__all__ = ['Tipo_Campos']

################################################################################

class Tipo_Campos (DeclarativeBase):
    """
    Definicion de tipos de campos

    """

    __tablename__ = 'Tabla_Tipo_Campos'

################################################################################

    #{ Columns

    id_tipo_campos = Column(Integer, autoincrement=True, primary_key=True)

    id_tipo_item = Column(Integer)

    nombre_campo =Column(Unicode(50),  nullable=False)

    valor_campo =Column(Unicode(50),  nullable=False)

################################################################################
    
    #{ Special methods

    def __repr__(self):
        return '<Tipo campos : id=%s>' % self.id_tipo_campos

    def __unicode__(self):
        return self.id_tipo_campos

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_campos(self):
        """
        Permite obtener todos los tipos de campos.
        """
        campos = DBSession.query(Tipo_Campos).all()
        return campos
    print get_tipo_campos.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_campo_by_tipo_item_por_pagina(self,
                        id_tipo_item,start=0,end=5):
        """
        Obtiene el tipo de campo por tipo de item.
        """
        tipos = DBSession.query(Tipo_Campos).slice(start,end).all()
        lista=[]
        for tipo_campo in tipos:
            if tipo_campo.id_tipo_item == id_tipo_item:
                lista.append(tipo_campo)

        return lista
    print get_tipo_campo_by_tipo_item_por_pagina.__doc__ 

#-------------------------------------------------------------------------------


    @classmethod
    def get_campos_by_tipo_item(self, id_tipo):
        """
        Obtiene los campos por tipo de item.
        """
        campos = DBSession.query(Tipo_Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_tipo_item == id_tipo):
                lista.append(campo)
        return lista
    print get_campos_by_tipo_item.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombres_by_tipo_item(self, id_tipo):
        """
        Obtiene los nombres por el tipo de item.
        """
        campos = DBSession.query(Tipo_Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_tipo_item == id_tipo):
                lista.append(campo.nombre_campo)
        return lista
    print get_nombres_by_tipo_item.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_campo_by_id(self,id_campo):
        """
        Obtiene los tipos de campos a través de su identificador.
        """
        campo = DBSession.query(Tipo_Campos).get(int(id_campo))

        return campo
    print get_campo_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_campo):
        """
        Elimina el tipo de campo.         
        """
        DBSession.delete(DBSession.query(Tipo_Campos).get(id_campo))
        DBSession.flush()
    print borrar_by_id.__doc__ 	

#-------------------------------------------------------------------------------

################################################################################

