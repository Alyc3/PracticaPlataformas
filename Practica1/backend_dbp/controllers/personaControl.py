from models.persona import Persona
from models.rol import Rol
from models.cuenta import Cuenta
from controllers.utils.errors import Erros
import uuid
from app import db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class PersonaControl:

    # Metodo para listar personas
    def listar(self):
        return Persona.query.all()
    
    # Metodo para guardar persona
    def guardar_cliente(self, data):
        persona = Persona()
        rol = Rol.query.filter_by(nombre="CLIENTE").first()
        if rol:
            persona.external_id = str(uuid.uuid4())
            persona.nombres = data.get('nombres')
            persona.apellidos = data.get('apellidos')
            persona.identificacion = data.get('identificacion')
            persona.direccion = data.get('direccion')
            persona.telefono = data.get('telefono')
            persona.id_rol = rol.id
            db.session.add(persona)
            db.session.commit()
            return persona.id
        return -1

    
    # Metodo para guardar un censador
    def guardar_admin(self, data):
        persona = Persona()
        rol = Rol.query.filter_by(nombre="ADMINISTRADOR").first()
        if rol:
            cuenta = Cuenta.query.filter_by(correo = data.get('correo')).first()
            if cuenta:
                return -2
            else:
                # Persona
                persona.external_id = str(uuid.uuid4())
                persona.nombre = data.get('nombres')
                persona.apellido = data.get('apellidos')
                persona.estado = data.get('estado')
                persona.identificacion = data.get('identificacion')
                persona.id_rol = rol.id
                db.session.add(persona)
                db.session.commit()
                # Cuenta
                cuenta_new = Cuenta()
                cuenta_new.correo = data.get('correo')
                cuenta_new.clave = data.get('clave')
                cuenta_new.external_id = str(uuid.uuid4())
                cuenta_new.id_persona = persona.id
                db.session.add(cuenta_new)
                db.session.commit()
                return cuenta_new.id
        else:
            return -1
        
    # Metodo para obtener una persona por external_id
    def obtener_por_external_id(self, external_id):
        return Persona.query.filter_by(external_id=external_id).first()
    
    def modificar_cuenta(self, data,external_id):
        cuenta = Cuenta.query.filter_by(external_id=external_id).first()
        if cuenta:
            persona = Persona.query.filter_by(id=cuenta.id_persona).first()
            if persona:
                persona.apellidos = data.get("apellidos", persona.apellidos)
                persona.nombres = data.get("nombres", persona.nombres)
                cuenta.correo = data.get("correo", cuenta.correo)
                cuenta.clave = data.get("clave", cuenta.clave)
                db.session.commit()
                return cuenta.id
            else:
                return -3  # Persona no encontrada
        else:
            return -2  # Cuenta no encontrada
    # Metodo para modificar una persona por id
    def modificar(self, external_id, data):
        # 1. Ob Persona
        persona = Persona.query.filter_by(external_id=external_id).first()

        # 2. Validar existe persona
        if persona:
            # 3. Actualizar atributos de persona
            persona.nombres = data.get('nombres', persona.nombres)
            persona.apellidos = data.get('apellidos', persona.apellidos)
            persona.fecha_nac = data.get('fecha_nac', persona.fecha_nac)
            persona.estado = data.get('estado', persona.estado)
            persona.id_rol = data.get('id_rol', persona.id_rol)

            # 4. Update
            db.session.commit()

            return persona
        else:
            # 5. Retornar -3 en caso de error
            return -3
        # Metodo para activar una cuenta
        
    def activar_cuenta(self, external_id):
        cuenta = Cuenta.query.filter_by(external_id=external_id).first()
        if cuenta:
            cuenta.estado = True
            db.session.commit()
            return cuenta
        else:
            return None
    
    # Metodo para desactivar una cuenta
    def desactivar_cuenta(self, external_id):
        cuenta = Cuenta.query.filter_by(external_id=external_id).first()
        if cuenta:
            cuenta.estado = False
            db.session.commit()
            return cuenta
        else:
            return None
        
    def inicio_sesion(self, data):
        cuentaA = Cuenta.query.filter_by(correo = data.get('correo')).first()
        if cuentaA:
            # TODO encriptar
            if cuentaA.clave == data["clave"]:
                token = jwt.encode(
                    {
                        "external": cuentaA.external_id,
                        "expiracion": (datetime.utcnow() + timedelta(minutes=30)).isoformat()
                    }, 
                    key = current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )

                cuenta = Cuenta.query.get(cuentaA.id)
                persona = cuenta.getPersona(cuentaA.id_persona)
                info = {
                    "token": token,
                    "user": persona.apellidos + " " + persona.nombres,
                    "external_id": persona.external_id
                }
                return info
            else:
                return -5
        else:
            return -5