# -*- coding: utf-8 -*-
"""
Fase* related model.


It's perfectly fine to re-use this definition in the Saip application,
though.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text , String
from sqlalchemy.orm import relation, synonym
from saip2011.model import DeclarativeBase, metadata, DBSession
from saip2011.model.proyecto import Proyecto , proyecto_tipo_fase_tabla
from saip2011.model.tipo_item import Tipo_Item , tipo_fase_tipo_item_tabla


__all__ = ['Tipo_Fase']


class Tipo_Fase(DeclarativeBase):
    """
    Definicion de Fase.

    """

    __tablename__ = 'Tabla_Tipo_Fase'

    #{ Columns

    id_tipo_fase = Column(Integer, autoincrement=True, primary_key=True)

    nombre_tipo_fase = Column(Unicode(50), unique=True, nullable=False)

    descripcion = Column(Text)

     #{ Relations

    proyectos = relation(Proyecto, secondary=proyecto_tipo_fase_tabla,
	                  backref='tipos_fases')

    tipos_items = relation(Tipo_Item, secondary=tipo_fase_tipo_item_tabla,
	                  backref='tipos_fases')



    #{ Special methods

    def __repr__(self):
	    return '<Fase: Nombre=%s>' % self.nombre_tipo_fase

    def __unicode__(self):
	    return self.nombre_tipo_fase

    @classmethod
    def get_tipo_fase(self):
	    """
	    Obtiene la lista de todos los roles
	    registrados en el sistema
	    """

	    tipos_fases = DBSession.query(Tipo_Fase).all()
	        
	    return tipos_fases

    @classmethod
    def get_tipo_fase_por_pagina(self,start=0,end=5):
        """
        Obtiene la lista de todos los roles
        registrados en el sistema
        """

        tipos_fases = DBSession.query(Tipo_Fase).slice(start,end).all()
            
        return tipos_fases

    @classmethod
    def get_tipo_fase_by_id(self,tipo_fase_id):
        """
        Obtiene la lista de todos los usuarios
        registrados en el sistema
        """
        tipos_fases = DBSession.query(Tipo_Fase).all()
        for tipo_fase in tipos_fases:
            if tipo_fase.id_tipo_fase == tipo_fase_id:
                return tipo_fase


    #}

