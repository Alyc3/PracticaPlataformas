from controllers.utils.errors import Erros
from models.sucursal import Sucursal
import uuid
from app import db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class SucursalControl:
    # Metodo para listar personas
    def listar(self):
        return Sucursal.query.all()
    
    def guardarSucursal(self, data):
        sucursal = Sucursal()
        sucursal.external_id = str(uuid.uuid4())
        sucursal.nombre = data.get('nombre')
        sucursal.latitud = data.get('latitud')
        sucursal.longitud = data.get('longitud')
        db.session.add(sucursal)
        db.session.commit()
        return sucursal.id
        
    