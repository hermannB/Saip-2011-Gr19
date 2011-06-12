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

# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
equipo_fases_tabla = Table('Tabla_Equipo_Fases', metadata,
    Column('id_equipo', Integer, ForeignKey('Tabla_Equipo_Desarrollo.id_equipo',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_fase', Integer, ForeignKey('Tabla_Fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE"))
)


class Equipo_Desarrollo(DeclarativeBase):
	"""
	Definicion de Equipo de Desarrollo.

	"""

	__tablename__ = 'Tabla_Equipo_Desarrollo'

	#{ Columns

	id_equipo = Column(Integer, autoincrement=True, primary_key=True)

	proyecto = Column(Integer)

	idusuario = Column(Integer, ForeignKey('Tabla_Usuario.idusuario'))

	nombre_usuario = relation('Usuario', backref='Equipo_Desarrollo')

	idrol = Column(Integer, ForeignKey('Tabla_Rol.idrol'))

	nombre_rol = relation('Rol', backref='Equipo_Desarrollo')
    
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


	@classmethod
	def get_miembros_by_proyecto(self, id_proyecto):
		equipos = DBSession.query(Equipo_Desarrollo).all()
		lista = []
		for equipo in equipos:
			if (equipo.proyecto == id_proyecto):
				lista.append(equipo)
		return lista

	@classmethod
	def get_miembro(self, id_miembro):
		equipos = DBSession.query(Equipo_Desarrollo).all()

		for equipo in equipos:
			if (equipo.idusuario == id_miembro):
				return equipo

	
    #}

	@classmethod
	def get_miembros_by_usuario(self, id_miembro):
		equipos = DBSession.query(Equipo_Desarrollo).all()
		lista = []
		for equipo in equipos:
			if (equipo.idusuario == id_miembro):
				lista.append(equipo)

		return lista


#
