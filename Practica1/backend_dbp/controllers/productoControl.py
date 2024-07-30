from models.persona import Persona
from models.producto import Producto
from models.lote import Lote
from controllers.utils.errors import Erros
import uuid
from app import db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class ProductoControl:

    # Metodo para listar personas
    def listar(self):
        return Producto.query.all()
    
    def guardarProducto(self,data,external):
        # Obtén el lote con el nombre dado
        persona = Persona.query.filter_by(external_id = external).first()
        if persona :
            lote = Lote.query.filter_by(external_id = data.get("external_lote")).first()
            if lote:
                producto = Producto()
                producto.nombre = lote.nombrePr
                producto.descripcion = data.get('descripcion')
                producto.precio = data.get('precio')
                producto.stock = lote.cantidadL 
                producto.persona_id = persona.id
                producto.id_lote = lote.id
                print(producto.persona)
                producto.external_id = uuid.uuid4()
                db.session.add(producto)
                db.session.commit()
                return producto.id
            
        else: 
            return -8
        
    