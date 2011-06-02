from formencode import Schema, validators

class UsuarioForm(Schema):
    alias = validators.UnicodeString(not_empty=True)
    nombre = validators.UnicodeString(not_empty=True)
    apellido = validators.UnicodeString(not_empty=True)
    nacionalidad = validators.UnicodeString(not_empty=False)
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
        
