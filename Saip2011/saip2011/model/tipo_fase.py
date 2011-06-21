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
    Definición de Tipo_Fase.

    """

    __tablename__ = 'Tabla_Tipo_Fase'

################################################################################

    #                   Columnas

    id_tipo_fase = Column(Integer, autoincrement=True, primary_key=True)

    nombre_tipo_fase = Column(Unicode(50), unique=True, nullable=False)

    descripcion = Column(Text)

################################################################################

     #                  Relaciones

    proyectos = relation(Proyecto, secondary=proyecto_tipo_fase_tabla,
                      backref='tipos_fases')

    tipos_items = relation(Tipo_Item, secondary=tipo_fase_tipo_item_tabla,
                      backref='tipos_fases')

################################################################################

    #                   Metodos

    def __repr__(self):
        return '<Fase: Nombre=%s>' % self.nombre_tipo_fase

    def __unicode__(self):
        return self.nombre_tipo_fase

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_fases(self):
        """
        Obtiene todos los tipos de fases.
        """
        tipos_fases = DBSession.query(Tipo_Fase).all()
        return tipos_fases
    print get_tipo_fases.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_fase_by_id(self,tipo_fase_id):
        """
        Obtiene un Tipo de Fase a través de su identificador.
        """
        tipos_fases = DBSession.query(Tipo_Fase).all()
        for tipo_fase in tipos_fases:
            if tipo_fase.id_tipo_fase == tipo_fase_id:
                return tipo_fase
    print get_tipo_fase_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_fase_por_pagina(self,start=0,end=5):
        """
        Obtiene los tipos de fase.
        """

        tipos_fases = DBSession.query(Tipo_Fase).slice(start,end).all()
            
        return tipos_fases
    print get_tipo_fase_por_pagina.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_tipo_fase_por_filtro(self,param,texto,start=0,end=5):
        """
        Obtiene un Tipo de Fase a través del nombre o la descripción del Tipo de Fase.
        """
        
        if param == "nombre":
            tipos_fases = DBSession.query(Tipo_Fase).filter(Tipo_Fase.nombre_tipo_fase.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "descripcion":
            tipos_fases = DBSession.query(Tipo_Fase).filter(Tipo_Fase.descripcion.like('%s%s%s' % ('%',texto,'%'))).all()
                    
        return tipos_fases
    print get_tipo_fase_por_filtro.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_tipo_fase):
        """
        Elimina el Tipo de Fase.         
        """
        DBSession.delete(DBSession.query(Tipo_Fase).get(id_tipo_fase))
        DBSession.flush()
    print borrar_by_id.__doc__ 	

#-------------------------------------------------------------------------------
################################################################################
