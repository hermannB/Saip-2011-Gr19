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

__all__ = ['EquipoDesarrollo']


#{ Association tables



class EquipoDesarrollo(DeclarativeBase):
    """
   Definicion de Equipo de Desarrollo.
    
    """
    
    __tablename__ = 'tabla_equipodesarrollo'
    
    #{ Columns
    
    idequipo = Column(Integer, autoincrement=True, primary_key=True)
    
    alias = Column(Unicode(30), unique=True, nullable=False)
    
    rol = Column(Unicode(30), nullable=False)
    
    
    #{ Relations
    
#    users = relation('User', secondary=user_group_table, backref='groups')
    
    #{ Special methods
    
    def __repr__(self):
        return '<Equipo : id=%s>' % self.idequipo
    
    def __unicode__(self):
        return self.idequipo
    
    #}


#
