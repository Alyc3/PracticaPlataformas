from models.estadoPr import EstadoPr
from models.producto import Producto
from models.sucursal import Sucursal
from models.lote import Lote
from controllers.utils.errors import Erros
from flask import jsonify, request
from werkzeug.utils import secure_filename
import os
import uuid
from app import db
import jwt
from datetime import datetime, timedelta
from flask import current_app

class LoteControl:

    # Metodo para listar lotes
    def listar(self):
        return Lote.query.all()
    #Metodo para poder buscar por external id
    def obtener_por_external_id(self, external_id):
        return Lote.query.filter_by(external_id=external_id).first()
    
    def obtenerLoteSucursal(self, external_id):
        sucursal = Sucursal.query.filter_by(external_id=external_id).first()
        if sucursal:
            lotes = Lote.query.filter_by(id_sucursal=sucursal.id).all()
            if lotes:
                productos = []
                for lote in lotes:
                    productos.extend(Producto.query.filter_by(id_lote=lote.id).all())
                print(f"Productos: {productos}")
                return productos
            
    def obteneEstadoProducto(self, external_id):
        sucursal = Sucursal.query.filter_by(external_id=external_id).first()
        if sucursal:
            lotes = Lote.query.filter_by(id_sucursal=sucursal.id,estadoPr="Vencido").all()
            if  lotes:
                return lotes
              
        
    # Metodo para guardar lote
    def guardar(self, data, file, external_id):
        try:
            # Obtener datos del formulario
            data = request.form
            file = request.files.get('file')
    
            # Crear instancia de Lote
            lote = Lote()
            
            # Buscar la sucursal por external_id
            sucursal = Sucursal.query.filter_by(external_id=external_id).first()
            print(f"Sucursal: {sucursal}")
            if sucursal:
                # Asignar atributos del lote
                lote.id_sucursal = sucursal.id
                lote.nombrePr = data.get('nombrePr')
                
                fechaPr = data.get('fechaPr')
                if fechaPr:
                    lote.fechaPr = datetime.strptime(fechaPr, '%d/%m/%Y').strftime('%Y-%m-%d')
                
                fechaVen = data.get('fechaVen')
                if fechaVen:
                    lote.fechaVen = datetime.strptime(fechaVen, '%d/%m/%Y').strftime('%Y-%m-%d')
                
                lote.cantidadL = data.get('cantidadL')
                lote.estadoPr = 'Buen_Estado'
                lote.external_id = uuid.uuid4()
                print(f"Sucursal : {sucursal.id}")
                
                # Guardar imagen si existe
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    rel_path = os.path.join('image', filename)
                    abs_file_path = os.path.join(os.getcwd(), rel_path)
                    file.save(abs_file_path)
                    lote.imagen = abs_file_path
    
                # Guardar lote en la base de datos
                db.session.add(lote)
                db.session.commit()
                
                return lote.id
            else:
                return {"error": "Sucursal no encontrada"}
        except Exception as e:
            print(f"Error al guardar lote: {e}")
            return -1
        
    
    def listar_PorCaducar(self):
        hoy = datetime.now().date()
        lotes = Lote.query.all()
        lotes_por_caducar = []
        for lote in lotes:
            if lote.fechaVen is not None:
                if lote.fechaVen - timedelta(days=5) <= hoy < lote.fechaVen:
                    lote.estadoPr = 'PorCaducar'
                    lotes_por_caducar.append(lote)
                elif lote.fechaVen == hoy:
                    lote.estadoPr = 'Vencido'
                    lotes_por_caducar.append(lote)
            db.session.commit()
        return lotes_por_caducar
    
    def listar_vencidos(self):
        # Obtén la fecha actual
        hoy = datetime.now().date()
        # Obtén todos los lotes
        lotes = Lote.query.all()
        lotes_vencidos = []
        for lote in lotes:
            
            # Verifica si el lote está vencido o por vencer
            if lote.fechaVen.date() < hoy or (lote.fechaVen.date() == hoy and lote.estadoPr != 'Vencido'):
                lote.estadoPr = "Vencido"
                productos_del_lote = Producto.query.filter_by(id_lote=lote.id).all()
                # Actualiza el stock de todos los productos en el lote a 0
                for producto in productos_del_lote:
                    producto.stock = 0
                print(f"Lote actualizado: {lote.nombrePr}, Estado: {lote.estadoPr}")
                lotes_vencidos.append(lote.serialize)
    
        db.session.commit()
    
        return lotes_vencidos
    
    def listar_LVencido(self):
       return Lote.query.filter_by(estadoPr='Vencido').all()
    
    def listar_estados(self):
        return [e.value for e in EstadoPr]
    
    def subir_imagen_lote(self, external_id):
        lote = self.obtener_por_external_id(external_id)
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'}), 400
        file = request.files['imagen']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(r'C:\Users\Edison\Desktop\PlataformasU1\PlataformasU1\Practica1\backend_dbp\image', filename)
            file.save(filepath)
            
            if lote:
                lote.imagen = filepath
                db.session.add(lote)
                db.session.commit()
                return jsonify({'mensaje': 'Archivo subido exitosamente'}), 200
            else:
                return jsonify({'error': 'Lote no encontrado'}), 404

    
    
