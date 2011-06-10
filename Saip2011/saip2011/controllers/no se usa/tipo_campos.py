










# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @expose('saip2011.templates.tipo_item.listar_tipo_campos')
    def listar_tipo_campos(self):
        """Lista campos del tipo de item
        """
        id_tipo_item = Tipo_Item.get_ultimo_id()
	if id_tipo_item is None:
           id_tipo_item=0
	id_tipo_item=1+id_tipo_item

	tipos_campos= Tipo_Campos.get_campos_by_tipo_item(id_tipo_item)

        return dict(pagina="listar_tipo_campos",tipos_campos=tipos_campos)

    @expose('saip2011.templates.tipo_item.editar_tipo_campos')
    def editar_tipo_campos(self,id_tipo_campos,*args, **kw):
	tipo_campos = DBSession.query(Tipo_Campos).get(id_tipo_campos)

	if request.method != 'PUT':  

	  values = dict(id_tipo_campos=tipo_campos.id_tipo_campos, 
	  	        nombre_campo=tipo_campos.nombre_campo, 
                        valor_campo=tipo_campos.valor_campo,
                    )

	  return dict(pagina="editar_tipo_campos",values=values)

    @validate({'id_tipo_campos':Int(not_empty=True),
	       'nombre_campo':NotEmpty, 
               'valor_campo':Int(not_empty=True),}, error_handler=editar_tipo_campos)	

    @expose()
    def put_tipo_campos(self, id_tipo_campos, nombre_campo, valor_campo, **kw):
	tipo_campos = DBSession.query(Tipo_Campos).get(id_tipo_campos)

	
        tipo_campos.nombre_campo = nombre_campo
        tipo_campos.valor_campo = valor_campo

        DBSession.flush()
        flash("Campo modificado!")
	redirect('/agregar_tipo_item')

    @expose('saip2011.templates.tipo_item.eliminar_tipo_campos')
    def eliminar_tipo_campos(self,id_tipo_campos, *args, **kw):
        tipo_campos = DBSession.query(Tipo_Campos).get(id_tipo_campos)

	values = dict(id_tipo_campos=tipo_campos.id_tipo_campos, 
	  	        nombre_campo=tipo_campos.nombre_campo, 
                        valor_campo=tipo_campos.valor_campo,
                    )

        return dict(pagina="eliminar_tipo_campos",values=values)

    @validate({'id_tipo_campos':Int(not_empty=True), 
	       'nombre_campo':NotEmpty, 
               'valor_campo':Int(not_empty=True),}, error_handler=eliminar_tipo_campos)

    @expose()
    def post_delete_tipo_campos(self, id_tipo_campos, nombre_campo, valor_campo, **kw):

        DBSession.delete(DBSession.query(Tipo_Campos).get(id_tipo_campos))
        DBSession.flush()
        flash("Campo eliminado!")
	redirect('/tipo_item')

    @expose('saip2011.templates.tipo_item.agregar_tipo_campos')
    def agregar_tipo_campos(self,cancel=False,**data):
        errors = {}
        tipo_campos = None

        if request.method == 'POST':
            if cancel:
                redirect('/tipo_item')
            form = TipoCamposForm()
            try:
                data = form.to_python(data)
		
		id_tipo_item = Tipo_Item.get_ultimo_id()
		if id_tipo_item is None:
		   id_tipo_item=0
		
		id_tipo_item=1+id_tipo_item
                tipos_campos = Tipo_Campos(id_tipo_item=id_tipo_item, nombre_campo=data.get('nombre_campo'),
				      valor_campo=data.get('valor_campo'))

                DBSession.add(tipos_campos)
                DBSession.flush()
                print tipo_campos
                flash("Campo agregado!")
		redirect('/agregar_tipo_item')

            except Invalid, e:
                print e
                tipo_campos = None
                errors = e.unpack_errors()
                flash(_("Favor complete los datos requeridos"),'warning')

            except IntegrityError:
                flash("LLave duplicada")
                DBSession.rollback()
                redirect('/agregar_tipo_item')
        else:
            errors = {}        

        return dict(pagina='agregar_tipo_campos',data=data.get('nombre_campo'),errors=errors)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
