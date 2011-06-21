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

__all__ = ['Variables']

################################################################################

class Variables (DeclarativeBase):
    """
    Definicion de las variables.

    """

    __tablename__ = 'Tabla_Variables'

################################################################################
    
    #               Columnas

    id_variable = Column(Integer, autoincrement=True, primary_key=True)

    nombre =Column(Unicode(50),  nullable=False)

    valor =Column(Unicode(50),  nullable=False)

################################################################################

    #               Metodos

    def __repr__(self):
        return '<Variables : id=%s>' % self.id_variable

    def __unicode__(self):
        return self.nombre

#-------------------------------------------------------------------------------

    @classmethod
    def get_variables(self):
        """
        Obtiene la lista de todos los equipos
        registrados en el sistema
        """

        var = DBSession.query(Variables).all()
        return var

    print get_variables.__doc__

#-------------------------------------------------------------------------------
    @classmethod
    def get_valor_by_nombre(self, nombre):
        """
            Obtiene el valor de la variable por el nombre.
        """ 
        variables = DBSession.query(Variables).all()
            for var in variables:
                if (var.nombre == nombre):
                    return var.valor
    print get_valor_by_nombre.__doc__

#-------------------------------------------------------------------------------
    @classmethod
    def set_valor_by_nombre(self, nombre, valor):
        """
        Setea el nombre de una variable.
        """

        variables = DBSession.query(Variables).all()
        for var in variables:
            if (var.nombre == nombre):
                var.valor=valor
                DBSession.flush()

    print set_valor_by_nombre.__doc__

#-------------------------------------------------------------------------------
