# -*- coding: utf-8 -*-
"""Item Controller"""

from tg import expose, flash, require, url, request, redirect
from datetime import datetime
import time
from tg.decorators import expose, validate
from formencode.validators import DateConverter, Int, NotEmpty

from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what import predicates
import transaction
from saip2011.lib.base import BaseController
from saip2011.model import DBSession, metadata

from saip2011 import model
from saip2011.model.auth import Usuario , Rol , Privilegios
from saip2011.model.fase import Fase
from saip2011.model.tipo_fase import Tipo_Fase
from saip2011.model.item import Item
from saip2011.model.variables import Variables
from saip2011.model.adjunto import Adjunto
from saip2011.model.equipo_desarrollo import Equipo_Desarrollo
from saip2011.model.tipo_item import Tipo_Item
from saip2011.model.proyecto import Proyecto
from saip2011.model.historial import Historial
from saip2011.model.tipo_campos import Tipo_Campos
from saip2011.model.campos import Campos
from saip2011.model.relaciones import Relaciones
from saip2011.model.linea_base import Linea_Base
from cherrypy import HTTPRedirect
from genshi.template import TemplateLoader
import os
from saip2011.form import UsuarioForm , RolForm , PrivilegioForm , FaseForm 
from saip2011.form import ItemForm , TipoItemForm , EquipoForm , ProyectoForm 
from saip2011.form import TipoFaseForm , TipoCamposForm
from formencode import Invalid
from psycopg2 import IntegrityError
from saip2011.controllers.error import ErrorController
import base64
import binascii


class ItemController(BaseController):
    

################################################################################
    @expose('saip2011.templates.item.item')
    def item(self,start=0,end=5,indice=None,texto=""):
        """
        Menu para Item
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        paginado = 5
        if start <> 0:
            end=int(start.split('=')[1]) #obtiene el fin de pagina
            start=int(start.split('&')[0]) #obtiene el inicio de pagina
        #print start,end
        
        pagina_actual = ((start % end) / paginado) + 1
        if ((start % end) % paginado) <> 0:
             pagina_actual = pagina_actual + 1
                         
        if indice  <> None and texto <> "":  
            fases=Fase.get_fase_by_proyecto_por_filtro(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")), indice,texto )
            total = len(fases)
        else:   
            fases,total=Fase.get_fase_by_proyecto_por_pagina(int (Variables.get_valor_by_nombre
                                                ("proyecto_actual")), start,end )

            #total = len(Fase.get_fase_by_proyecto(int (Variables.get_valor_by_nombre
             #                                   ("proyecto_actual")) ))

        lista = ['nombre','descripcion']
        
        return dict(pagina="listar_fase",fases=fases,nom_proyecto=nom_proyecto
                                ,nom_fase=nom_fase,inicio=start,fin=end,
                                pagina_actual=pagina_actual,paginado=paginado,
                                total=total,param="/item/item",lista=lista)
    print item.__doc__

###############################################################################

    @expose('saip2011.templates.item.listar_mis_adjuntos')
    def ver_adjuntos(self,id_item):
        """Lista los adjuntos del item dado.  
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        item=Item.get_item_by_id(id_item)

        values = dict(id_item=item.id_item, 
				        nombre_item=item.nombre_item, 
				        nombre_tipo_item=item.nombre_tipo_item
				        )

        adjuntos=Adjunto.get_adjuntos_by_item(id_item)
       
        return dict(pagina="listar_mis_adjuntos",adjuntos=adjuntos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)
    print ver_adjuntos.__doc__

###############################################################################
        
    @expose('saip2011.templates.item.listar_item')
    def listar_item_activos (self):
        """
        Lista todos los items activos.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_item_activados_by_fase(id_fase)
        ids=0
        for i in items:
            ids=i.id_item

        return dict(pagina="listar_item",items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
    print listar_item_activos.__doc__

################################################################################

    @expose('saip2011.templates.item.historial')
    def historial (self, id_item):
        """
        Muestra el historial de un item.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_historial(id_item)

        return dict(pagina="historial",items=items,nom_proyecto=nom_proyecto
                    ,nom_fase=nom_fase)
    print historial.__doc__

################################################################################

    @expose('saip2011.templates.item.listar_item eliminados')
    def listar_item_eliminados(self):
        """Lista lso items eliminados.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        items = Item.get_item_eliminados_by_fase(id_fase)

        return dict(pagina="listar_item eliminados",items=items,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    print listar_item_eliminados.__doc__

################################################################################

    @expose('saip2011.templates.item.editar_item')
    def editar_item(self,id_item,*args, **kw):
        """
        Permite la edición de un item.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        id_fase=int (Variables.get_valor_by_nombre("fase_actual") )

        if id_item is not None:
            id_item=int(id_item)

        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
        item = Item.get_item_by_id(id_item)
        fase = Fase.get_fase_by_id(id_fase)	

        orden=str(fase.orden)

        padres=Relaciones.get_padres_habilitados(fase.orden)   
        hijos=Relaciones.get_sucesores(id_item)
       
        master=[]
        if (fase.orden ==1):
            master.append(Item.get_master().id_item)
        else:
            master.append(0)

        for hijo in hijos:                                                      #evita que yo o algun sucesor sea mi nuevo padre
            if hijo in padres:
                padres.remove(hijo)
        for padre in padres:
            if padre.id_item == id_item:
                padres.remove(padre)

        tipos_items=fase.tipos_items

        lista=[]
        lista.append(item.id_tipo_item )

        values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
                        nombre_tipo_item=item.nombre_tipo_item,        
						codigo_item=item.codigo_item,
						estado=item.estado,
						complejidad=item.complejidad,
						)

        adjuntos=Adjunto.get_adjuntos_by_item(item.id_item)
 
        adjuntados=[]
        for adj in adjuntos:        
            var = dict(id_adjunto=adj.id_adjunto,
                            nombre_archivo=adj.nombre_archivo)
            adjuntados.append(var)
       
        padres2=[]        
        padr=Relaciones.get_mis_padres(id_item)
        for pad in padr:
            padres2.append(pad.id_item)

        campos= Campos.get_campos_by_item(id_item)

        return dict(pagina="editar_item",values=values,adjuntados=adjuntados,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        lista=lista,tipos_items=tipos_items,padres=padres,
                        padres2=padres2,master=master,orden=orden,campos=campos)
    print editar_item.__doc__

#-------------------------------------------------------------------------------

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'complejidad':Int(not_empty=True)}, error_handler=editar_item)

#-------------------------------------------------------------------------------

    @expose('saip2011.templates.item.editar_item')
    def put_item(self, id_item, nombre_item, nombre_tipo_item, complejidad,
                    id_campos,nombre_campo,tipo_campo,dato,
                     padres,asmSelect0,adjunto=None,adjuntados=None):
        """
        Permite la edición de un item.
        """

        if id_item is not None:
            id_item=int(id_item)


        item = Item.get_item_by_id(id_item)
        items= Item.get_nombres_items()
        items.remove(item.nombre_item)
        
        if nombre_item not in items:

            if id_campos is not None:
                if not isinstance(id_campos, list):
                    id_campos = [id_campos]

            if nombre_campo is not None:
                if not isinstance(nombre_campo, list):
                    nombre_campo = [nombre_campo]

            if tipo_campo is not None:
                if not isinstance(tipo_campo, list):
                    tipo_campo = [tipo_campo]

            if dato is not None:
                if not isinstance(dato, list):
                    dato = [dato]


            if complejidad is not None:
                complejidad=int(complejidad)

            if adjuntados is not None:
                if not isinstance(adjuntados, list):
                    adjuntados = [adjuntados]
                if len(adjuntados)<1:
                    adjuntados =[]

            if adjunto is not None:
                if not isinstance(adjunto, list):
                    adjunto = [adjunto]

            if padres is not None:
                if not isinstance(padres, list):
                    padres = [padres]
                padres = [DBSession.query(Item).get(padre) for padre
                                         in padres]


            item.estado_oculto="Desactivado"
            DBSession.flush()

            version=item.version+1

            item2 = Item (nombre_item=nombre_item ,
                         codigo_item=item.codigo_item ,
                         id_tipo_item=item.id_tipo_item , 
                         complejidad=complejidad,
                         estado = item.estado ,
                         orden=item.orden,
                         fase=int(Variables.get_valor_by_nombre
                                ("fase_actual")),
                         proyecto=int(Variables.get_valor_by_nombre
                                ("proyecto_actual")),
                         creado_por=Variables.get_valor_by_nombre
                                ("usuario_actual"),
                        fecha_creacion = time.ctime() ,
                        version =version ,estado_oculto="Activo",
                        lb_parcial=item.lb_parcial,lb_general=item.lb_general)

            DBSession.add(item2)
            DBSession.flush()

            indice=0
            id_item=Item.get_ultimo_id()        
            for c in id_campos:
                if len(c)>0:
                    camp =Campos(id_item=id_item,
                                    nombre_campo=nombre_campo[indice],
                                    tipo_campo=tipo_campo[indice],
                                    dato=dato[indice])
                    DBSession.add(camp)
                    indice+=1

            mayor =Item.get_ultimo_id()
            relacion = Relaciones (id_item_hijo=mayor,padres=padres)

            if adjunto is not None:
                for adj in adjunto:
                    if len(str(adj))==0:
                        break
                    if len(adj.filename)==0:
                        break
                    data = adj.file.read()
                    encode=base64.b64encode(data)
                    var=binascii.a2b_base64(encode)
                    adj = Adjunto (id_item=mayor, archivo=var,
                                    nombre_archivo=adj.filename,version=item2.version,
                                    estado_oculto=item2.estado_oculto)

                    DBSession.add(adj)
                    DBSession.flush() 

            adjuntos=Adjunto.get_adjuntos_by_item(item.id_item)
            for adjun in adjuntos:
                if adjuntados is not None:
                    if adjun.nombre_archivo in adjuntados:
                        adj2 = Adjunto(id_item=mayor,archivo=adjun.archivo,
                                       nombre_archivo=adjun.nombre_archivo,
                                       version=item2.version, 
                                       estado_oculto=item2.estado_oculto    )
                        DBSession.add(adj2)
                        DBSession.flush() 
                
                adjun.estado_oculto=item.estado_oculto
                DBSession.flush()

            flash("Item Modificado!")
            redirect('/item/item')

        else:
            nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
            nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

            padres=Item.get_item_activados()                                        #cambiar esta funcion y solo traer lo que no forman ciclos
            id_fase=int(Variables.get_valor_by_nombre("fase_actual"))          
            fase = Fase.get_fase_by_id(id_fase)	
            tipos_items=fase.tipos_items

            lista=[]
            lista.append(item.nombre_tipo_item )
            item = DBSession.query(Item).get(id_item)

            values = dict(id_item=id_item, 
				            nombre_item=nombre_item,        
				            codigo_item=item.codigo_item,
    			            complejidad=complejidad,
				            )

            adjuntos=Adjunto.get_adjuntos_by_item(item.id_item)
     
            adjuntados=[]
            for adj in adjuntos:        
                var = dict(id_adjunto=adj.id_adjunto,
                                nombre_archivo=adj.nombre_archivo)
                adjuntados.append(var)

            padres2=[]        
            padr=Relaciones.get_mis_padres(id_item)
            for pad in padr:
                padres2.append(pad.id_item)

            flash("EL NOMBRE DEL ITEM YA EXISTE!")
            return dict(pagina="editar_item",values=values,adjuntados=adjuntados,
                            nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                            lista=lista,tipos_items=tipos_items,padres=padres,
                            padres2=padres2)
    print put_item.__doc__


################################################################################

    @expose('saip2011.templates.item.eliminar_item')
    def eliminar_item(self,id_item, *args, **kw):
        """
        Elimina un item dado.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        item = DBSession.query(Item).get(id_item)	

        values = dict(id_item=id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)

        return dict(pagina="eliminar_item",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    print eliminar_item.__doc__

#-------------------------------------------------------------------------------

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty, 
				'codigo_item':NotEmpty, 
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item
				)

#-------------------------------------------------------------------------------

    @expose()
    def post_delete_item(self, id_item, nombre_item, codigo_item, nombre_tipo_item,
                         estado, complejidad, **kw):
        """
        Permite la eliminación de un item dado.
        """

        if id_item is not None:
            id_item=int(id_item)

        item = Item.get_item_by_id(id_item)
        item.estado_oculto="Eliminado"

        DBSession.flush()

        flash("Item eliminado!")
        redirect('/item/item')
    print post_delete_item.__doc__

################################################################################

    @expose('saip2011.templates.item.revivir_item')
    def revivir_item(self,id_item, *args, **kw):
        """
        Permite revivir un item dado.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        item = Item.get_item_by_id(id_item)	

        values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)

        return dict(pagina="revivir_item",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    print revivir_item.__doc__

#-------------------------------------------------------------------------------

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'codigo_item':NotEmpty,  
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item)

#-------------------------------------------------------------------------------

    @expose()
    def post_revivir_item(self, id_item, nombre_item , codigo_item, 
                            nombre_tipo_item, estado, complejidad, **kw):
        """
        Permite revivir un item dado.
        """
        item = Item.get_item_by_id(id_item)
        item.estado_oculto="Activo"

        DBSession.add(item)
        DBSession.flush()

        flash("Item Revivido!")
        redirect('/item/item')
    print post_revivir_item.__doc__

################################################################################

    @expose('saip2011.templates.item.recuperar_item')
    def recuperar_item(self,id_item, *args, **kw):
        """
        Recupera un item dado.
        """
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

        if id_item is not None:
            id_item=int(id_item)

        item = Item.get_item_by_id(id_item)	

        values = dict(id_item=item.id_item, 
						nombre_item=item.nombre_item,
						codigo_item=item.codigo_item,
						nombre_tipo_item=item.nombre_tipo_item, 
						estado=item.estado,
						complejidad=item.complejidad,
						)

        return dict(pagina="recuperar_item",values=values,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase)
    print recuperar_item.__doc__

#-------------------------------------------------------------------------------

    @validate({'id_item':Int(not_empty=True),
				'nombre_item':NotEmpty,
				'codigo_item':NotEmpty,  
				'complejidad':Int(not_empty=True), 
				'estado':NotEmpty}, error_handler=eliminar_item
				 )

#-------------------------------------------------------------------------------

    @expose()
    def post_recuperar_item(self, id_item, nombre_item, codigo_item, 
                nombre_tipo_item, estado, complejidad, **kw):
        """
        Permite la recuperación de un item dado.
        """

        if id_item is not None:
            id_item=int(id_item)

        if complejidad is not None:
            complejidad=int(complejidad)

        item = Item.version_actual(id_item)
        item.estado_oculto="Desactivado"
        version= item.version+1  

        DBSession.flush()

        item2 = Item.get_item_by_id(id_item)

        item3 = Item (nombre_item=item2.nombre_item,
                        codigo_item=item2.codigo_item, 
                        id_tipo_item=item2.id_tipo_item,
                        orden=item2.orden,
						complejidad=item2.complejidad, estado = item2.estado,
                        fase=item2.fase, proyecto=item2.proyecto,
                        creado_por =item2.creado_por, 
                        fecha_creacion = item2.fecha_creacion ,
                        version =version , estado_oculto="Activo",
                        lb_parcial=item2.lb_parcial,lb_general=item2.lb_general)
	
        DBSession.add(item3)
        DBSession.flush()
        
        adjuntos=Adjunto.get_adjuntos_by_item(item.id_item)
        for adjun in adjuntos:
            adjun.estado_oculto=item.estado_oculto
            DBSession.flush()

        mayor =Item.get_ultimo_id()
        adjuntos=Adjunto.get_adjuntos_by_item(item2.id_item)
        for adjun in adjuntos:
            adj2 = Adjunto(id_item=mayor,archivo=adjun.archivo,
                           nombre_archivo=adjun.nombre_archivo,
                           version=item3.version, 
                           estado_oculto=item3.estado_oculto    )
            DBSession.add(adj2)
            DBSession.flush() 


        flash("Item recuperado!")
        redirect('/item/item')
    print post_recuperar_item.__doc__

################################################################################

    @expose('saip2011.templates.item.agregar_item')
    def agregar_item(self, *args, **kw):
        """
        Agrega un item a la fase.
        """
        nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
        nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
        id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
       

        fase = Fase.get_fase_by_id(id_fase)
        orden=str(fase.orden)

        padres=Relaciones.get_padres_habilitados(fase.orden)   
       
        master=[]
        
        if (fase.orden ==1):
            master.append(Item.get_master().id_item)
        else:
            master.append(0)
        tipos_items=fase.tipos_items

        return dict(pagina="agregar_item",values=kw, tipos_items=tipos_items
                    ,nom_proyecto=nom_proyecto,nom_fase=nom_fase,padres=padres,
                    master=master,orden=orden)
    print agregar_item.__doc__

#-------------------------------------------------------------------------------
    
    @validate({'nombre_item':NotEmpty, 
			    'complejidad':Int(not_empty=True)}, error_handler=agregar_item
			    )

#-------------------------------------------------------------------------------

    @expose('saip2011.templates.item.agregar_item')
    def post_item(self, nombre_item, complejidad, adjunto, id_tipo_item,
                    asmSelect0,padres=None):
        """
        Permite agregar un nuevo item a la fase.
        """

        items= Item.get_nombres_items()

        if nombre_item not in items:
        
            if id_tipo_item is not None:
                id_tipo_item = int(id_tipo_item)

            if complejidad is not None:
                complejidad=int(complejidad)

            if adjunto is not None:
                if not isinstance(adjunto, list):
                    adjunto = [adjunto]

            if padres is not None:
                if not isinstance(padres, list):
                    padres = [padres]
                padres = [DBSession.query(Item).get(padre) for padre
                                         in padres]


#----------------------------------------

            tipo_item =Tipo_Item.get_tipo_item_by_id(id_tipo_item)
            pre_codigo=tipo_item.codigo_tipo_item

            proy_act=int (Variables.get_valor_by_nombre("proyecto_actual"))
            fas_act=int (Variables.get_valor_by_nombre("fase_actual"))
            fase=Fase.get_fase_by_id(fas_act)

            codigo_item=Item.crear_codigo(id_tipo_item,
                                            pre_codigo,proy_act,fas_act)

            item = Item (nombre_item=nombre_item, codigo_item=codigo_item,
                            id_tipo_item=id_tipo_item, 
	                        complejidad=complejidad, estado = "nuevo", 
                            fase=fas_act,proyecto=proy_act,orden=fase.orden,
	                        creado_por=Variables.get_valor_by_nombre("usuario_actual"),
	                        fecha_creacion = time.ctime(), version =1 ,
                            estado_oculto="Activo",lb_parcial=0,lb_general=0
	                        )

            DBSession.add(item)
            DBSession.flush()

#----------------------------------------

            for padre in padres:
                if padre.nombre_item == "master":
                    padres.remove(padre)
           
            mayor =int(Item.get_ultimo_id())
        
            relacion = Relaciones (id_item_hijo=mayor,padres=padres)

#----------------------------------------
            id_item2=Item.get_ultimo_id()        
            tipos_campos=Tipo_Campos.get_campos_by_tipo_item(id_tipo_item)

            for tipo in tipos_campos:
                camp =Campos(id_item=id_item2,
                             nombre_campo=tipo.nombre_campo,
                             tipo_campo= tipo.valor_campo)
                DBSession.add(camp)
            DBSession.flush()


#----------------------------------------

            if adjunto is not None:
                for adj in adjunto:
                    if len(str(adj))==0:
                        break
                    if len(adj.filename)==0:
                        break

                    data = adj.file.read()
                    encode=base64.b64encode(data)
                    var=binascii.a2b_base64(encode)
                    adj = Adjunto (id_item=mayor, archivo=var,
                                nombre_archivo=adj.filename, version =item.version ,
                                    estado_oculto=item.estado_oculto)

                    DBSession.add(adj)
                    DBSession.flush() 

            flash("Item Agregado!")  
            redirect('/item/item')

        else:

            nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")
            nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")

            id_fase=int(Variables.get_valor_by_nombre("fase_actual"))
            padres=Item.get_item_activados()                                        #cambiar esta funcion y solo traer lo que no forman ciclos
            fase = Fase.get_fase_by_id(id_fase)	
            tipos_items=fase.tipos_items

            values = dict(nombre_item=nombre_item,
						id_tipo_item=id_tipo_item, 
						complejidad=complejidad,
						)

            flash("Nombre de Item ya existente!")
            return dict(pagina="agregar_item",values=values,
                        tipos_items=tipos_items,nom_proyecto=nom_proyecto,
                        nom_fase=nom_fase,padres=padres)
    print post_item.__doc__

################################################################################

    @expose('saip2011.templates.item.listar_mis_adjuntos')
    def descargar(self, id_adjunto):
        """
        Permite la descarga de un archivo adjunto.
        """
        directorio = "/home/hermann/Descargas"

        adj = Adjunto.get_adjunto_by_id(id_adjunto)
        var=binascii.b2a_base64(adj.archivo)
        archivo=base64.b64decode(var)  
        filenameDest=directorio +"/"+str(adj.nombre_archivo)

        dirdescargavalido=self.validardir(directorio)

        # se crea el archivo y se procede a copiar el contendido del archivo
        
        if (dirdescargavalido):
            try:
             file = open(filenameDest, 'wb')        # crea el archivo destino
            except:
                return "No se pudo crear el archivo"   
            
            if not archivo: 
                return                                         
            file.write(archivo)                                 
                
            #se cierra la conexion y el archivo
                 
            file.close( )
            redirect('/item/item')

        else:

            nom_proyecto=Variables.get_valor_by_nombre("nombre_proyecto_actual")
            nom_fase=Variables.get_valor_by_nombre("nombre_fase_actual")

            item=Item.get_item_by_id(int(adj.id_item))
            values = dict(id_item=item.id_item, 
				            nombre_item=item.nombre_item, 
				            nombre_tipo_item=item.nombre_tipo_item
				            )

            return dict(pagina="listar_mis_adjuntos",adjuntos=adjuntos,
                        nom_proyecto=nom_proyecto,nom_fase=nom_fase,
                        values=values)
    print descargar.__doc__


################################################################################

    @expose()
    def validardir(self,dirdescarga):
        """
        Valida la dirección para la descarga de un adjunto.
        """
        if (os.path.isdir(dirdescarga)):
            return True
        else:
            try:
                os.mkdir(dirdescarga)
                return True
            except:
                print "No se puede crear el directorio"
                return False  
    print validardir.__doc__
    
################################################################################

