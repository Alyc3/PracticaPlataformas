from flask import Blueprint, jsonify, make_response, request
from controllers.personaControl import PersonaControl
from controllers.utils.errors import Erros
from flask_expects_json import expects_json
from controllers.authenticate import token_required

api_persona = Blueprint('api_persona', __name__)

# API para Persona
personaC = PersonaControl()

schema_sesion = {
    "type": "object",
    'properties': {
        "correo": {"type": "string"},
        "clave": {"type": "string"},
    },
    'required': ["correo", "clave"]
}

schema_cliente = {
    "type": "object",
    'properties': {
        "nombres": {"type": "string"},
        "apellidos": {"type": "string"},
        "identificacion": {"type": "string"},
        "direccion": {"type": "string"},
        "telefono": {"type": "integer"},
    },
    'required': ["nombres", "apellidos", "identificacion","direccion", "telefono"]
}
schema_admin = {
    "type": "object",
    'properties': {
        "nombres": {"type": "string"},
        "apellidos": {"type": "string"},
        "identificacion": {"type": "string"},
        "correo": {
            "type": "string",
            "pattern": r"^[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+([.][a-zA-Z0-9_]+)*[.][a-zA-Z]{2,5}$"
        },
        "clave": {"type": "string"},
    },
    'required': ["nombres", "apellidos", "identificacion", "correo", "clave"]
}



# API para listar personas
@api_persona.route("/persona")
@token_required
def listar():
    datos = [i.serialize() for i in personaC.listar()]
    if datos:
            return make_response(jsonify({"msg": "OK", "code": 200, "datos": datos}), 200)
    else:
            return make_response(jsonify({"msg": "ERROR", "code": 404, "datos": {"error" : Erros.error[str(id)]}}), 404)

# API para mostrar persona por external_id
@api_persona.route("/persona/<external_id>")
def mostrar(external_id):
    persona = personaC.obtener_por_external_id(external_id)
    if persona is not None:
        persona = persona.serialize()
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": []if persona is None else persona}), 200)
    
@api_persona.route('/modificar_cuenta/<external_id>', methods=['POST'])
def modificar_cuenta_api(external_id):
    data = request.json
    result = personaC.modificar_cuenta(data,external_id)

    if result == -1:
        return jsonify({"error": "Role not found"}), 404
    elif result == -2:
        return jsonify({"error": "Account already exists"}), 409
    else:
        return jsonify({"msg": "OK", "code": 200, "datos": {"tag":"Datos Guardados"}}), 200



# API para guardar censador
@api_persona.route("/persona/guardar/admin", methods=['POST'])
@expects_json(schema_admin)
def guardar_admin():
    data = request.get_json()
    id = personaC.guardar_admin(data)
    print("el id es: "+ str(id))

    if id >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"tag": "Datos Guardados"}}),
            200
        )
    else:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Erros.error[str(id)]}}), 
            400
        )
    
@api_persona.route("/persona/guardar_cliente", methods=['POST'])
@expects_json(schema_cliente)
def guardar_cliente():
    data = request.get_json()
    id = personaC.guardar_cliente(data)

    if id >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"tag": "Datos Guardados"}}),
            200
        )
    else:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Erros.error[str(id)]}}), 
            400
        )

# API para modificar persona por external_id
@api_persona.route("/persona/modificar/<external_id>", methods=['POST'])
def modificar(external_id):
    data = request.get_json()
    persona = personaC.modificar(external_id, data)
    if persona:
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": persona.serialize()}), 200)
    else:
        return make_response(jsonify({"msg": "Error", "code": 404, "datos": {"error": "Persona no encontrada"}}), 404)


# API para desactivar una cuenta
@api_persona.route("/cuenta/desactivar/<external_id>", methods=['POST'])
def desactivar_cuenta(external_id):
    cuenta = personaC.desactivar_cuenta(external_id)
    if cuenta:
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": {"tag": "Cuenta desactivada"}}), 200)
    else:
        return make_response(jsonify({"msg": "Error", "code": 404, "datos": {"error": "Cuenta no encontrada"}}), 404)

# API para iniciar sesion
@api_persona.route("/sesion", methods=['POST'])
@expects_json(schema_sesion)
def session():
    data = request.json
    id = personaC.inicio_sesion(data)
    print("el id es: "+ str(id))

    if type(id) == int:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Erros.error[str(id)]}}), 
            400
        )
    else:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": id}),
            200
        )