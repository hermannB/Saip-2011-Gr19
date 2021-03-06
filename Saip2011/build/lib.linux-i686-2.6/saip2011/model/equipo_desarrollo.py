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


################################################################################

#           Tablas Intermedias para relaciones muchos a muchos

#   Tabla Equipo Desarroloo - Fase
equipo_fases_tabla = Table('Tabla_Equipo_Fases', metadata,
    Column('id_equipo', Integer, ForeignKey('Tabla_Equipo_Desarrollo.id_equipo',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_fase', Integer, ForeignKey('Tabla_Fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE"))
)

################################################################################

class Equipo_Desarrollo(DeclarativeBase):
    """
    Definicion de Equipo de Desarrollo.

    """

    __tablename__ = 'Tabla_Equipo_Desarrollo'

################################################################################


    #               Columnas

    id_equipo = Column(Integer, autoincrement=True, primary_key=True)

    proyecto = Column(Integer)

    idusuario = Column(Integer, ForeignKey('Tabla_Usuario.idusuario'))

    nombre_usuario = relation('Usuario', backref='Equipo_Desarrollo')

    idrol = Column(Integer, ForeignKey('Tabla_Rol.idrol'))

    nombre_rol = relation('Rol', backref='Equipo_Desarrollo')


################################################################################
    #                   Metodos

    def __repr__(self):
        return '<Equipo : id=%s>' % self.id_equipo

    def __unicode__(self):
        return self.id_equipo

#-------------------------------------------------------------------------------

    @classmethod
    def get_equipos(self):
        """
        Obtiene la lista de todos los equipos
        registrados en el sistema
        """
        equipos = DBSession.query(Equipo_Desarrollo).all()
        return equipos    

#-------------------------------------------------------------------------------

    @classmethod
    def get_miembros_by_proyecto_por_pagina(self,id_proyecto,start=0,end=5):
        """
        Obtiene la lista de todos los roles
        registrados en el sistema
        """
        equipos = DBSession.query(Equipo_Desarrollo).all()
            
        lista = []
        c = 0
        for equipo in equipos:
            if (equipo.proyecto == id_proyecto):
                c = c + 1
                if c < end and c > start-1:
                    
                    lista.append(equipo)
                    
        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_miembros_by_proyecto_por_filtro(self,id_proyecto,param,texto):
        """
        Obtiene la lista de todos los roles
        registrados en el sistema
        """
        equipos = DBSession.query(Equipo_Desarrollo).all()
            
        lista = []
        for equipo in equipos:
            if (equipo.proyecto == id_proyecto):
                lista.append(equipo)
        
        lista_filtrada = []
        if param=="nombre":
            for equipo in lista:
                if texto in equipo.nombre_usuario.alias:
                    lista_filtrada.append(equipo)
                    
       
        return lista_filtrada


#-------------------------------------------------------------------------------

    @classmethod
    def get_miembros_by_proyecto(self, id_proyecto):
        equipos = DBSession.query(Equipo_Desarrollo).all()
        lista = []
        for equipo in equipos:
	        if (equipo.proyecto == id_proyecto):
		        lista.append(equipo)
        return lista

#-------------------------------------------------------------------------------


    @classmethod
    def get_miembro_by_id(self, id_miembro):
        equipos = DBSession.query(Equipo_Desarrollo).all()
        for equipo in equipos:
            if (equipo.id_equipo == id_miembro):
                return equipo

#-------------------------------------------------------------------------------

    @classmethod
    def get_miembros_by_usuario(self, id_miembro):
        equipos = DBSession.query(Equipo_Desarrollo).all()
        lista = []
        for equipo in equipos:
            if (equipo.idusuario == id_miembro):
	            lista.append(equipo)

        return lista

#-------------------------------------------------------------------------------

    @classmethod
    def get_miembro_by_usuario_by_proyecto(self, id_usuario,id_proyecto):
        equipos = DBSession.query(Equipo_Desarrollo).all()
        lista = []
        for equipo in equipos:
            if(equipo.idusuario == id_usuario and equipo.proyecto==id_proyecto):
                return equipo
#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_miembro):
        """
        Obtiene la lista de todos los adjuntos         
        """
        DBSession.delete(DBSession.query(Equipo_Desarrollo).get(id_miembro))
        DBSession.flush()	

#-------------------------------------------------------------------------------


