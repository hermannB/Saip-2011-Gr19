# -*- coding: utf-8 -*-
"""
Proyecto * related model.

"""

import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Text
from sqlalchemy.orm import relation, synonym


from saip2011.model.equipo_desarrollo import Equipo_Desarrollo

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Proyecto']

################################################################################
            #Tabla Intermedia para relaciones muchos a muchs
#   tabla Proyecto - Tipo Fase

proyecto_tipo_fase_tabla = Table('Tabla_Proyecto_Tipo_Fase', metadata,
    Column('id_proyecto', Integer, ForeignKey('Tabla_Proyecto.id_proyecto',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_tipo_fase', Integer, ForeignKey('Tabla_Tipo_Fase.id_tipo_fase',
        onupdate="CASCADE", ondelete="CASCADE"))
)

################################################################################

class Proyecto(DeclarativeBase):
    """

    Definición del Proyecto

    """

    __tablename__ = 'Tabla_Proyecto'

################################################################################

    #                       Columnas

    id_proyecto = Column(Integer, autoincrement=True, primary_key=True)

    nombre_proyecto = Column(Unicode(50), unique=True, nullable=False)

    descripcion = Column(Text)	

    idusuario = Column(Integer, ForeignKey('Tabla_Usuario.idusuario'))

    lider_equipo = relation('Usuario', backref='Proyecto')

    estado = Column(Unicode(50),  nullable=False)

################################################################################

    #                       Metodos

    def __repr__(self):
	    return '<Proyecto: nombre=%s>' % self.nombre_proyecto

    def __unicode__(self):
	    return self.nombre_proyecto

#-------------------------------------------------------------------------------

    @classmethod
    def get_proyectos(self):
        """
        Obtiene todos los proyectos.
        """

        proyectos = DBSession.query(Proyecto).all()
        return proyectos

    print get_proyectos.__doc__
    
#-------------------------------------------------------------------------------

    @classmethod
    def get_proyectos_by_equipo_desarrollo(self,idusuario):
        """
        Obtiene los proyectos en los que el usuario enviado como parámetro forma parte.
        """

        proy = DBSession.query(Proyecto).all()
        proyectos = []
        miembros=Equipo_Desarrollo.get_miembros_by_usuario(idusuario)

        for miembro in miembros:
            for p in proy:
                if (miembro.proyecto == p.id_proyecto):
                    proyectos.append(p)
        
        return proyectos

    print get_proyectos_by_equipo_desarrollo.__doc__
    
#-------------------------------------------------------------------------------

    @classmethod
    def get_proyectos_by_equipo_desarrollo_por_pagina(self,idusuario,start=0,end=5):
        """
        Obtiene los proyectos en los que el usuario forma parte.
        """

        #obtengo los proyectos del usuario actual
        proyectos = Proyecto.get_proyectos_by_equipo_desarrollo(idusuario)
        
        lista_paginada = []
        c = 0
        for proy in proyectos:
            if c < end and c > start-1:
                lista_paginada.append(proy) 
            c = c + 1

        return lista_paginada, len(proyectos)

    print get_proyectos_by_equipo_desarrollo_por_pagina.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_proyectos_by_equipo_desarrollo_por_filtro(self,idusuario,param,texto):
        """
        Obtiene los proyectos en los que está asignado el usuario. La búsqueda se realiza por nombre o por descripción 
        del proyecto.
        """

        #obtengo los proyectos del usuario actual
        proyectos = Proyecto.get_proyectos_by_equipo_desarrollo(idusuario)
        
        lista_filtrada = []
        
        if param=="nombre":
            for proy in proyectos:
                if texto in proy.nombre_proyecto:
                    lista_filtrada.append(proy) 
            
        elif param=="descripcion":     
            for proy in proyectos:
                if texto in proy.descripcion:
                    lista_filtrada.append(proy)
                    
        return lista_filtrada

    print get_proyectos_by_equipo_desarrollo_por_filtro.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_proyecto_by_id(self,id_proyecto):
        """
        Obtiene el proyecto buscado por su identificador.
        """

        proyecto = DBSession.query(Proyecto).get(id_proyecto)
        return proyecto

    print get_proyecto_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_proyectos_por_pagina(self,start=0,end=5):
        """
        Obtiene una lista de los proyectos
        """

        proyectos = DBSession.query(Proyecto).slice(start,end).all()

        return proyectos

    print get_proyectos_por_pagina.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_proyectos_por_filtro(self,param,texto):
        """
        Obtiene los proyectos buscados por nombre o descripción del proyecto.
        """

        if param == "nombre":
            proyectos = DBSession.query(Proyecto).filter(Proyecto.nombre_proyecto.like('%s%s%s' % ('%',texto,'%'))).all()
        elif param == "descripcion":
            proyectos = DBSession.query(Proyecto).filter(Proyecto.descripcion.like('%s%s%s' % ('%',texto,'%'))).all()
            
        return proyectos

    print get_proyectos_por_filtro.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_nombres(self):
        """
        Obtiene los nombres de los proyectos.
        """

        proyectos = DBSession.query(Proyecto).all()
        lista=[]

        for proyecto in proyectos:
            lista.append(proyecto.nombre_proyecto) 

        return lista

    print get_nombres.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_ultimo_id(self):
        """
        Obtiene el ultimo id de la tabla Proyecto
        """

        mayor =0
        proyectos = DBSession.query(Proyecto).all()

        for proy in proyectos:
            if (proy.id_proyecto > mayor):
                mayor = proy.id_proyecto
        return mayor

    print get_ultimo_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def activar(self, id_proyecto):
        proyecto = DBSession.query(Proyecto).get(id_proyecto)
        if proyecto.estado =="nuevo":
            proyecto.estado="en_desarrollo"
            DBSession.flush()

#-------------------------------------------------------------------------------

    @classmethod
    def finalizar(self, id_proyecto):
        proyecto = DBSession.query(Proyecto).get(id_proyecto)
        if proyecto.estado =="en_desarrollo":
            proyecto.estado="finalizado"
            DBSession.flush()

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_proyecto):
        """
        Obtiene la lista de todos los proyecto         
        """

        DBSession.delete(DBSession.query(Proyecto).get(id_proyecto))
        DBSession.flush()	

#-------------------------------------------------------------------------------

################################################################################
