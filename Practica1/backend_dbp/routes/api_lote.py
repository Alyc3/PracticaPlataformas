from controllers.authenticate import token_required
from flask import Blueprint, jsonify, make_response, request
from controllers.loteControl import LoteControl
from controllers.utils.errors import Erros
from flask_expects_json import expects_json
from werkzeug.utils import secure_filename
import os

api_lote = Blueprint('api_lote', __name__)

# API para Motivo
loteC = LoteControl()
# Validadores
schema = {
    "type": "object",
    'properties': {
        "nombrePr": {"type": "string"},
        "fechaPr": {"type": "string"},
        "fechaVen": {"type": "string"},
        "cantidadL": {"type": "integer"},
    },
    'required': ["nombrePr","fechaPr", "fechaVen", "cantidadL"]
}

@api_lote.route("/lote")
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize() for i in loteC.listar()]}),
        200
    )
@api_lote.route("/lote/por_caducar")
def listar_PorCaducar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in loteC.listar_PorCaducar()]}),
        200
    )
@api_lote.route("/lote/vencidos")
def listar_vencidos():
    try:
        lote = loteC.listar_vencidos()
        datos_serializados = [i.serialize() for i in lote if hasattr(i, 'serialize')]
        return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize() for i in loteC.listar_vencidos()]}),
        200)
    except Exception as e:
        return make_response(jsonify({"msg": "Error al serializar los datos", "code": 500, "error": str(e)}), 500
    )
    
    
@api_lote.route("/lote/guardarLote/<external_id>", methods=['POST'])
@token_required
def guardar(external_id):
    data = request.form.to_dict()
    file = request.files['file'] if 'file' in request.files else None
    id = loteC.guardar(data, file, external_id)

    if isinstance(id, int) and id >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"tag": "Datos Guardados"}}),
            200
        )
    
@api_lote.route("/lote/<external_id>")
def mostrar(external_id):
    lote = loteC.obtener_por_external_id(external_id)
    if lote:
        return make_response(jsonify({"msg": "OK", "code": 200, "datos": lote.serialize()}), 200)
    else:
        return make_response(jsonify({"msg": "Error", "code": 404, "datos": {"error": "Lote no encontrado"}}), 404)
    
@api_lote.route("/listar_estados", methods=['GET'])
def listar_estados():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": loteC.listar_estados()}),
        200
    )

@api_lote.route("/lote/subir_imagen_lote/<external_id>", methods=['POST'])
def subir_imagen_lote(external_id):
    if 'imagen' not in request.files:
        return jsonify({'error': 'No se encontró el archivo'}), 400
    file = request.files['imagen']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    if not (file.filename.endswith('.png') or file.filename.endswith('.jpg')):
        return jsonify({'error': 'Tipo de archivo no permitido. Solo se permiten archivos PNG y JPG.'}), 400
    
    file.seek(0, os.SEEK_END)  
    file_length = file.tell()
    if file_length > 5 * 1024 * 1024: 
        return jsonify({'error': 'El archivo supera el tamaño máximo permitido de 5MB'}), 400
    file.seek(0) 
    return loteC.subir_imagen_lote(external_id)


@api_lote.route("/lote/sucursal/<external_id>")
def listar_por_sucursal(external_id):
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize() for i in loteC.obtenerLoteSucursal(external_id)]}),
        200
    )
    
@api_lote.route("/estado_producto/<external_id>", methods=["GET"])
def obtener_estado_producto(external_id):
    lotes = loteC.obteneEstadoProducto(external_id)
    if lotes:
        return jsonify([lote.serialize() for lote in lotes]), 200
    else:
        return jsonify({"msg": "No se encontraron lotes vencidos", "code": 404}), 404