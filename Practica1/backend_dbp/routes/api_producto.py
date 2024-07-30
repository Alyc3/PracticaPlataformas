from controllers.authenticate import token_required
from flask import Blueprint, jsonify, make_response, request
from controllers.productoControl import ProductoControl
from controllers.utils.errors import Erros
from flask_expects_json import expects_json

api_producto = Blueprint('api_producto', __name__)

# API para Motivo
productoC = ProductoControl()
# Validadores
schema = {
    "type": "object",
    'properties': {
        "descripcion": {"type": "string"},
        "precio": {"type": "number"}
    },
    'required': ["descripcion","precio"]
}

@api_producto.route("/producto")
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize() for i in productoC.listar()]}),
        200
    )

@api_producto.route("/producto/guardarProducto/<external_id>", methods=['POST'])
@expects_json(schema)
def guardar(external_id):
    data = request.get_json()
    id = productoC.guardarProducto(data,external_id)
    if id > 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": id}),
            200
        )
    else:
        return make_response(
            jsonify({"msg": "Error", "code": 500, "datos": "No se pudo guardar el producto"}),
            500
        )
    
