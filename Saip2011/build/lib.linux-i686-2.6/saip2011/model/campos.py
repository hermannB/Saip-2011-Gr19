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

__all__ = ['Campos']


#{ Association tables



class Campos (DeclarativeBase):
    """
   Definicion de Campos para item.
    
    """
    
    __tablename__ = 'Tabla_Campos'
    
    #{ Columns
    
    id_campos = Column(Integer, autoincrement=True, primary_key=True)

    id_item = Column(Integer)
    
    nombre_campo =Column(Unicode(50),  nullable=False)

    valor_campo =Column(Unicode(50),  nullable=False)
   
   
    
    #{ Special methods
    
    def __repr__(self):
        return '<Campos : id=%s>' % self.id_campos
    
    def __unicode__(self):
        return self.id_campos


    @classmethod
    def get_campos(self):
        """
        Obtiene la lista de todos los campos
        registrados en el sistema
        """
        campos = DBSession.query(Campos).all()
        return campos


    @classmethod
    def get_campos_by_item(self, id_item):
        campos = DBSession.query(Campos).all()
        lista = []
        for campo in campos:
            if (campo.id_item == id_item):
                lista.append(campo)

        return lista
    #}

    #}

#
