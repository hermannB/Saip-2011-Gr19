from formencode import Schema, validators

class UsuarioForm(Schema):
    alias = validators.UnicodeString(not_empty=True)
    nombre = validators.UnicodeString(not_empty=True)
    apellido = validators.UnicodeString(not_empty=True)
    nacionalidad = validators.UnicodeString(not_empty=False)
    tipodocumento = validators.UnicodeString(not_empty=False)
    nrodoc = validators.UnicodeString(not_empty=False)
    clave = validators.UnicodeString(not_empty=True)
    clave2 = validators.UnicodeString(not_empty=True)
    email = validators.UnicodeString(not_empty=True)

class PrivilegioForm(Schema):
    nombreprivilegio = validators.UnicodeString(not_empty=True)
    descripcion = validators.UnicodeString(not_empty=True)

class RolForm(Schema):
    nombrerol = validators.UnicodeString(not_empty=True)
    descripcion = validators.UnicodeString(not_empty=True)
    privilegios = validators.UnicodeString(not_empty=True)


class FaseForm(Schema):
    nombre_fase = validators.UnicodeString(not_empty=True)
    tipo_fase = validators.UnicodeString(not_empty=True)
    estado = validators.UnicodeString(not_empty=True)
    linea_base = validators.UnicodeString(not_empty=True)
    descripcion = validators.UnicodeString(not_empty=True)


class TipoFaseForm(Schema):
    nombre_tipo_fase = validators.UnicodeString(not_empty=True)
    descripcion = validators.UnicodeString(not_empty=True)
    tipos_items = validators.UnicodeString(not_empty=True)

class ItemForm(Schema):
    nombre_item = validators.UnicodeString(not_empty=True)
    tipo_item = validators.UnicodeString(not_empty=True)
    fase = validators.UnicodeString(not_empty=True)
    proyecto = validators.UnicodeString(not_empty=False)
    adjunto = validators.UnicodeString(not_empty=False)
    complejidad = validators.UnicodeString(not_empty=True)
    estado = validators.UnicodeString(not_empty=True)
    campos = validators.UnicodeString(not_empty=True)
    lista_item = validators.UnicodeString(not_empty=True)
    creado_por = validators.UnicodeString(not_empty=True)
    fecha_creacion = validators.UnicodeString(not_empty=True)

class TipoItemForm(Schema):
    nombre_tipo_item = validators.UnicodeString(not_empty=True)
    descripcion = validators.UnicodeString(not_empty=True)

class EquipoForm(Schema):
    alias = validators.UnicodeString(not_empty=True)
    rol = validators.UnicodeString(not_empty=True)

class ProyectoForm(Schema):
    nombre_proyecto = validators.UnicodeString(not_empty=True)
    equipo = validators.UnicodeString(not_empty=True)
    lista_fases = validators.UnicodeString(not_empty=True)
    descripcion = validators.UnicodeString(not_empty=True)

class TipoCamposForm(Schema):
    nombre_campo = validators.UnicodeString(not_empty=True)
    id_tipo_item = validators.UnicodeString(not_empty=True)


