from controllers.authenticate import token_required
from flask import Blueprint, jsonify, make_response, request
from controllers.sucursalControl import SucursalControl
from controllers.utils.errors import Erros
from flask_expects_json import expects_json

api_sucursal = Blueprint('api_sucursal', __name__)

# API para Motivo
sucursalC = SucursalControl()
# Validadores
schema = {
    "type": "object",
    'properties': {
        "nombre": {"type": "string"},
        "latitud": {"type": "number"},
        "longitud": {"type": "number"},
    },
    'required': ["nombre","latitud","longitud"]
}

@api_sucursal.route("/sucursal")
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize() for i in sucursalC.listar()]}),
        200
    )

@api_sucursal.route("/sucursal/guardarSucursal", methods=['POST'])
@expects_json(schema)
def guardar():
    data = request.get_json()
    id = sucursalC.guardarSucursal(data)
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
    
