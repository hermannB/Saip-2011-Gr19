from formencode import Schema, validators

class UsuarioForm(Schema):
    alias = validators.UnicodeString(not_empty=True)
    nombre = validators.UnicodeString(not_empty=True)
    apellido = validators.UnicodeString(not_empty=True)
    nacionalidad = validators.UnicodeString(not_empty=False)
    nrodoc = validators.UnicodeString(not_empty=False)
    clave = validators.UnicodeString(not_empty=True)
    email = validators.UnicodeString(not_empty=True)
