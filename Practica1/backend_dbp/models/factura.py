from app import db
import uuid

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    fechaEmi = db.Column(db.DateTime)
    total = db.Column(db.Float)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable = False)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuenta.id'), nullable = False)
    # Relación uno a muchos con Detalle_Factura
   
    
    
    def serialize(self):
        return {
            'external_id': self.external_id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'total': self.total,
        }
    
    def copy(self):
        new_factura = Factura(
            id=self.id,
            fecha=self.fecha,
            total=self.total,
            external_id=self.external_id,
            id_persona=self.id_persona,
            id_cuenta=self.id_cuenta
        )
        return new_factura  