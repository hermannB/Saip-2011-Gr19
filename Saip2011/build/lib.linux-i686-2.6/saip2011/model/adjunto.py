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
    Definición de Adjunto
    """

    __tablename__ = 'Tabla_Adjunto'

    #                    Columnas

    id_adjunto = Column(Integer, autoincrement=True, primary_key=True)

    nombre_archivo= Column(Unicode(50))

    id_item = Column(Integer)

    version = Column(Integer)

    estado_oculto = Column(Unicode(50), nullable=False)

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
        registrados en el sistema.
        """
        lista=[]
        adjuntos = DBSession.query(Adjunto).all()
        for adj in adjuntos:
	        if( adj.id_item==id_item):
		        lista.append(adj)  
        return lista
print get_adjuntos_by_item.__doc__

#-------------------------------------------------------------------------------
@classmethod
def get_adjuntos(self):
        """
        Obtiene la lista de todos los adjuntos.         
        """
        adjuntos = DBSession.query(Adjunto).all()
        return adjuntos
print get_adjuntos.__doc__

#-------------------------------------------------------------------------------
@classmethod
def get_adjunto_by_item_por_pagina(self,id_item,start=0,end=5):
        """
        Obtiene la lista de todos los adjuntos por item.
        """
        adjuntos = DBSession.query(Adjunto).slice(start,end).all()
        lista=[]
        for    adjunto in adjuntos:
            if adjunto.id_item == id_item:
                lista.append(adjunto)

        return lista
print get_adjunto_by_item_por_pagina.__doc__

#-------------------------------------------------------------------------------
@classmethod
def get_adjunto_by_id(self,id_adjunto):
        """
        Obtiene la lista de todos los adjuntos por su identificador.
        """
        adjunto = DBSession.query(Adjunto).get(int(id_adjunto))
        return adjunto
print get_adjunto_by_id.__doc__

#-------------------------------------------------------------------------------
@classmethod
def borrar_by_id(self,id_adjunto):
        """
        Obtiene la lista de todos los adjuntos a través de su identificador.      
        """
        DBSession.delete(DBSession.query(Adjunto).get(id_adjunto))
        DBSession.flush()
print borrar_by_id.__doc__	

#-------------------------------------------------------------------------------
@classmethod
def guardar(self,adjunto):
        """
        Guarda el adjunto.         
        """
        DBSession.add(adjunto)
        DBSession.flush()
print guardar.__doc__

#-------------------------------------------------------------------------------
################################################################################

