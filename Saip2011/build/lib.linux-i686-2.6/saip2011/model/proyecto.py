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
	Column('idproyecto', Integer, ForeignKey('Tabla_Proyecto.idproyecto', onupdate="CASCADE", ondelete="CASCADE")),
	Column('idequipo', Integer, ForeignKey('Tabla_EquipoDesarrollo.idequipo', onupdate="CASCADE", ondelete="CASCADE"))
)

tabla_proyecto_fases = Table('TB_proyecto_fases', metadata,
	Column('idproyecto', Integer, ForeignKey('Tabla_Proyecto.idproyecto', onupdate="CASCADE", ondelete="CASCADE")),
	Column('idfase', Integer, ForeignKey('Tabla_Fase.idfase', onupdate="CASCADE", ondelete="CASCADE"))
)

class Proyecto(DeclarativeBase):
	"""

	Definicion del ṕroyecto

	"""

	__tablename__ = 'Tabla_Proyecto'

	#{ Columns

	idproyecto = Column(Integer, autoincrement=True, primary_key=True)

	nombreproyecto = Column(Unicode(30), unique=True, nullable=False)

	descripcion = Column(Text)	

	#{ Special methods

	def __repr__(self):
		return '<Proyecto: nombre=%s>' % self.nombreproyecto

	def __unicode__(self):
		return self.nombreproyecto

	#}

