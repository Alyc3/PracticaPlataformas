
from flask import Blueprint, jsonify, make_response,request
# Importacion de los modelos de tablas de la base de datos
from models.rol import Rol
from models.sucursal import Sucursal
from models.producto import Producto
from models.factura import Factura
from models.detalleFactura import DetalleFactura
from models.lote import Lote
from models.persona import Persona
from models.cuenta import Cuenta
from models.estadoPr import EstadoPr


api = Blueprint('api', __name__)

@api.route("/")
def home ():
    return make_response(
        jsonify({"msg": "OK", "code": 200}),
        200
    )

