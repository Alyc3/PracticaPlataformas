from app import db
import uuid

class DetalleFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    cantidad = db.Column(db.Integer)
    precioU = db.Column(db.Float)
    subTotal= db.Column(db.Float)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable = False)
    
    
    def serialize(self):
        return {
            'cantidad': self.cantidad,
            'precioU': self.precioU,
            'subTotal': self.subTotal,
        }
    
    def copy(self):
        new_detalle = DetalleFactura(
            id=self.id,
            cantidad=self.cantidad,
            precioU=self.precioU,
            subTotal=self.subTotal,
            external_id=self.external_id,
            id_factura=self.id_factura,
            id_producto=self.id_producto
        )
        return new_detalle