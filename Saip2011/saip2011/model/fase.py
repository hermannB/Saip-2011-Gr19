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
from saip2011.model.equipo_desarrollo import Equipo_Desarrollo
from saip2011.model.equipo_desarrollo import equipo_fases_tabla
from saip2011.model.tipo_item import Tipo_Item , fase_tipo_item_tabla

__all__ = ['Fase']

################################################################################

class Fase(DeclarativeBase):
    """
    Definicion de Fase.

    """

    __tablename__ = 'Tabla_Fase'

    #               Columnas

    id_fase = Column(Integer, autoincrement=True, primary_key=True)

    nombre_fase = Column(Unicode(50), nullable=False)

    id_tipo_fase = Column(Integer,ForeignKey('Tabla_Tipo_Fase.id_tipo_fase'))

    nombre_tipo_fase = relation('Tipo_Fase', backref='Fase')

    estado = Column(Unicode(50), nullable=False)

    proyecto = Column(Integer, nullable=False)

    orden = Column(Integer)

    linea_base =Column (Unicode(50), nullable=False)

    descripcion = Column(Text)

    equipo = relation(Equipo_Desarrollo, secondary=equipo_fases_tabla,
                      backref='fases')

    tipos_items = relation(Tipo_Item, secondary=fase_tipo_item_tabla,
                      backref='fases')

################################################################################

    #                   Metodos

    def __repr__(self):
        return '<Fase: Nombre=%s>' % self.nombre_fase

    def __unicode__(self):
        return self.nombre_fase

#-------------------------------------------------------------------------------
       
    @classmethod
    def get_fases(self):
        """
        Obtiene la lista de todas los fases
        registradas en el sistema
        """
        fases = DBSession.query(Fase).all()
        return fases
    print get_fases.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_fase_by_id(self,fase_id):
        """
        Obtiene una fase buscada por su identificador de fase.
        """
        fases = DBSession.query(Fase).all()
        for fase in fases:
            if fase.id_fase == fase_id:
                return fase
    print get_fase_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_fase_by_id(self,fase_id):
        """
        Obtiene una fase buscada por su identificador de fase.
        """
        fases = DBSession.query(Fase).all()
        for fase in fases:
            if fase.id_fase == fase_id:
                return fase
    print get_fase_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_fase_by_proyecto_por_pagina(self,id_proyecto,start=0,end=5):
        """
        Obtiene una lista de fases que pertenece a un proyecto dado.
        """
        #obtengo las fases del proyecto
        if id_proyecto is not None:
            id_proyecto = int(id_proyecto)

        fases = Fase.get_fase_by_proyecto(id_proyecto) 

        lista=[]
        c = 0
        for fase in fases:
            if c < end and c > start-1:
                lista.append(fase)
            c = c + 1    
                 
        return lista, len(fases)
    print get_fase_by_proyecto_por_pagina.__doc__

#-------------------------------------------------------------------------------
    
    @classmethod
    def get_fase_by_proyecto_por_filtro(self,id_proyecto,param,texto):
        """
        Obtiene la lista de fases de un proyecto, buscada por 'nombre', 'TipoFase' y 'Descripcion'.
        """
        """privilegios = session.query(cls).all()"""
        #privilegios = DBSession.query(Privilegios).all()
        
        if param == "nombre":
            fases = DBSession.query(Fase).filter(Fase.nombre_fase.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "TipoFase":
            fases = DBSession.query(Fase).filter(Fase.nombre_tipo_fase.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "descripcion":
            fases = DBSession.query(Fase).filter(Fase.descripcion.like('%s%s%s' % ('%',texto,'%'))).all()
           
        lista=[]
        for fase in fases:
            if fase.proyecto == id_proyecto:
                lista.append(fase)

        return lista
    print get_fase_by_proyecto_por_filtro.__doc__


#-------------------------------------------------------------------------------


    @classmethod
    def get_nombres_by_id(self,proyecto_id):
        """
        Obtiene la lista de nombres de fases de un proyecto dado.
        """
        fases = DBSession.query(Fase).all()
        lista=[]
        for fase in fases:
            if (fase.proyecto ==proyecto_id ):
                lista.append(fase.nombre_fase) 
        return lista
    print get_nombres_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_fase_by_proyecto(self,id_proyecto):
        """
        Obtiene una lista de fases por proyecto.
        """
        fases = DBSession.query(Fase).all()
        lista=[]
        for	fase in fases:
            if fase.proyecto == int(id_proyecto):
	            lista.append(fase)

        return lista
    print get_fase_by_proyecto.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_fase):
        """
        Elimina una fase dada-
        """
        DBSession.delete(DBSession.query(Fase).get(id_fase))
        DBSession.flush()	
    print borrar_by_id.__doc__

#-------------------------------------------------------------------------------


