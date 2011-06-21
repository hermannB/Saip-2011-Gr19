# -*- coding: utf-8 -*-
"""
Campos* related model.


"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Campos']


################################################################################

class Campos (DeclarativeBase):
    """
    Definicion de Campos para item.

    """

    __tablename__ = 'Tabla_Campos'

    #               Columnas

    id_campos = Column(Integer, autoincrement=True, primary_key=True)

    id_item = Column(Integer)

    nombre_campo =Column(Unicode(50),  nullable=False)

    tipo_campo =Column(Unicode(50),  nullable=False)

    dato =Column(Unicode(200))

################################################################################   
    
    #               Metodos

    def __repr__(self):
        return '<Campos : id=%s>' % self.id_campos

    def __unicode__(self):
        return self.id_campos

#-------------------------------------------------------------------------------

    @classmethod
    def get_campos(self):
        """
        Obtiene la lista de todos los campos
        registrados en el sistema
        """
        campos = DBSession.query(Campos).all()
        return campos
    print get_campos.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_campo_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los campos
        registrados en el sistema
        """

        campos = DBSession.query(Campos).slice(start,end).all()
            
        return campos
    print get_campo_por_pagina.__doc__


#-------------------------------------------------------------------------------

    @classmethod
    def get_campos_by_item(self, id_item):
        """
        Obtiene los campos de un item.
        """
        campos = DBSession.query(Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_item == id_item):
                lista.append(campo)
        return lista
    print get_campos_by_item.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_campo_by_id(self,id_campo):
        """
        Obtiene el campo por medio de su identificador de campo.         
        """
        campo = DBSession.query(Campo).get(int(id_campo))
        return campo
    print get_campo_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_campos):
        """
        Elimina un campo.
        """
        DBSession.delete(DBSession.query(Campos).get(id_campos))
        DBSession.flush()	

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombres_by_item(self, id_item):
        """
        Obtiene los nombres de campos por item
        """
        campos = DBSession.query(Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_item == id_item):
                lista.append(campo.nombre_campo)

        return lista
    print get_nombres_by_item.__doc__

#-------------------------------------------------------------------------------
