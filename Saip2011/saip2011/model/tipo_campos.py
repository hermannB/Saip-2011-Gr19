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
        Obtiene la lista de todos los equipos
        registrados en el sistema
        """
        campos = DBSession.query(Tipo_Campos).all()
        return campos

#-------------------------------------------------------------------------------

    @classmethod
    def get_campos_by_tipo_item(self, id_tipo):
        campos = DBSession.query(Tipo_Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_tipo_item == id_tipo):
                lista.append(campo)
        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombres_by_tipo_item(self, id_tipo):
        campos = DBSession.query(Tipo_Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_tipo_item == id_tipo):
                lista.append(campo.nombre_campo)
        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_campo_by_id(self,id_campo):
        """
        Obtiene la lista de todos los campo         
        """
        campo = DBSession.query(Tipo_Campos).get(int(id_campo))
        return campo

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_campo):
        """
        Obtiene la lista de todos los adjuntos         
        """
        DBSession.delete(DBSession.query(Tipo_Campos).get(id_campo))
        DBSession.flush()	

#-------------------------------------------------------------------------------

################################################################################

