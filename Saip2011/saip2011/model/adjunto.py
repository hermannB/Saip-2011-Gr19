# -*- coding: utf-8 -*-
"""
Adjunto* related model.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text , LargeBinary
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Adjunto']

################################################################################

class Adjunto(DeclarativeBase):
    """
    Definicion de Adjunto
    """

    __tablename__ = 'Tabla_Adjunto'

    #                    Columnas

    id_adjunto = Column(Integer, autoincrement=True, primary_key=True)

    nombre_archivo= Column(Unicode(50))

    id_item = Column(Integer)

    archivo = Column(LargeBinary, nullable=False)

################################################################################

    #                   Metodos

    def __repr__(self):
        return '<Adjunto: id=%s>' % self.id_adjunto

    def __unicode__(self):
        return self.id_adjunto

#-------------------------------------------------------------------------------
    
    @classmethod
    def get_adjuntos_by_item(self,id_item):
        """
        Obtiene la lista de todos los adjuntos del item
        registrados en el sistema
        """
        lista=[]
        adjuntos = DBSession.query(Adjunto).all()
        for adj in adjuntos:
	        if( adj.id_item==id_item):
		        lista.append(adj)  
        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_adjuntos(self):
        """
        Obtiene la lista de todos los adjuntos         
        """
        adjuntos = DBSession.query(Adjunto).all()
        return adjuntos

#-------------------------------------------------------------------------------

    @classmethod
    def get_adjunto_by_id(self,id_adjunto):
        """
        Obtiene la lista de todos los adjuntos         
        """
        adjunto = DBSession.query(Adjunto).get(int(id_adjunto))
        return adjunto

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_adjunto):
        """
        Obtiene la lista de todos los adjuntos         
        """
        DBSession.delete(DBSession.query(Adjunto).get(id_adjunto))
        DBSession.flush()	

#-------------------------------------------------------------------------------

    @classmethod
    def guardar(self,adjunto):
        """
        Obtiene la lista de todos los adjuntos         
        """
        DBSession.add(adjunto)
        DBSession.flush()

#-------------------------------------------------------------------------------
################################################################################

