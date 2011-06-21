# -*- coding: utf-8 -*-
"""
Historial* related model.

"""
import os
from datetime import datetime
import sys

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime , Text
from sqlalchemy.orm import relation, synonym

from saip2011.model import DeclarativeBase, metadata, DBSession

__all__ = ['Historial']



class Historial(DeclarativeBase):
    """
    Definición de Historial.

    """

    __tablename__ = 'Tabla_Historial'

################################################################################

    #               Columnas

    id_historial = Column(Integer, autoincrement=True, primary_key=True)

    id_item = Column(Integer, nullable=False)

    version = Column(Integer, nullable=False)

    creado_por = Column(Unicode(50), nullable=False)

    fecha_creacion = Column(DateTime, default=datetime.now)

    descripcion = Column(Text)

################################################################################

    #                   Metodos

    def __repr__(self):
	    return '<Historial: id_Historial=%s>' % self.id_historial

    def __unicode__(self):
	    return self.id_historial

#-------------------------------------------------------------------------------

    @classmethod
    def get_historiales(self):
        """
        Obtiene la lista de todos los historiales
        registrados en el sistema
        """

        historiales = DBSession.query(Historial).all()
            
        return historiales

    print get_historiales.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_historial_by_id(self,historial_id):
        """
        Obtiene un historial a traves de su identificador.
        """

        historiales = DBSession.query(Historial).all()
        for historial in historiales:
            if historial.id_historial == historial_id:
                return historiales

    print get_historial_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_historial_by_id(self,id_historial):
        """
        Obtiene un historial a traves de su identificador.
        """

        historial = DBSession.query(Historial).get(int(id_historial))
        return historial

    print get_historial_by_id.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def get_historiales_by_id_item(self,id_item):
        """
        Obtiene la lista de todos los historiales de un item a través de su identificador.
        """

        lista=[]
        historiales = DBSession.query(Historial).all()

        for historial in historiales:
            if historial.id_item == id_item:
                pos=historial.version-1
                lista.insert(pos,historial)

        return lista

    print get_historiales_by_id_item.__doc__

#-------------------------------------------------------------------------------

    @classmethod
    def borrar_by_id(self,id_historial):
        """
        Elimina un historial.
        """

        DBSession.delete(DBSession.query(Historial).get(id_historial))
        DBSession.flush()	

    print borrar_by_id.__doc__

#-------------------------------------------------------------------------------

