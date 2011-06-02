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

__all__ = ['Equipo_Desarrollo']


#{ Association tables



class Equipo_Desarrollo(DeclarativeBase):
    """
   Definicion de Equipo de Desarrollo.
    
    """
    
    __tablename__ = 'Tabla_Equipo_Desarrollo'
    
    #{ Columns
    
    id_equipo = Column(Integer, autoincrement=True, primary_key=True)
    
    alias = Column(Unicode(50), unique=True, nullable=False)
    
    rol = Column(Unicode(50), nullable=False)
    
    
    #{ Relations
    
#    users = relation('User', secondary=user_group_table, backref='groups')
    
    #{ Special methods
    
    def __repr__(self):
        return '<Equipo : id=%s>' % self.id_equipo
    
    def __unicode__(self):
        return self.id_equipo


    @classmethod
    def get_equipo(self):
        """
        Obtiene la lista de todos los equipos
        registrados en el sistema
        """

        equipos = DBSession.query(Equipo_Desarrollo).all()
           
        return equipos    
    #}


#
