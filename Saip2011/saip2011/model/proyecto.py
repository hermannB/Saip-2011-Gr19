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

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Proyecto']

tabla_proyecto_equipo = Table('TB_proyecto_equipo', metadata,
	Column('id_proyecto', Integer, ForeignKey('Tabla_Proyecto.id_proyecto', onupdate="CASCADE", ondelete="CASCADE")),
	Column('id_equipo', Integer, ForeignKey('Tabla_EquipoDesarrollo.id_equipo', onupdate="CASCADE", ondelete="CASCADE"))
)

tabla_proyecto_fases = Table('TB_proyecto_fases', metadata,
	Column('id_proyecto', Integer, ForeignKey('Tabla_Proyecto.id_proyecto', onupdate="CASCADE", ondelete="CASCADE")),
	Column('id_fase', Integer, ForeignKey('Tabla_Fase.id_fase', onupdate="CASCADE", ondelete="CASCADE"))
)

class Proyecto(DeclarativeBase):
	"""

	Definicion del ṕroyecto

	"""

	__tablename__ = 'Tabla_Proyecto'

	#{ Columns

	id_proyecto = Column(Integer, autoincrement=True, primary_key=True)

	nombre_proyecto = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column(Text)	

	#{ Special methods

	def __repr__(self):
		return '<Proyecto: nombre=%s>' % self.nombre_proyecto

	def __unicode__(self):
		return self.nombre_proyecto

	#}

