from app import db
import uuid
from datetime import datetime

class Producto (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(250))
    precio = db.Column(db.Float)
    stock= db.Column(db.Integer)    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relación uno a muchos con Producto_Persona
    persona_id= db.Column(db.Integer, db.ForeignKey('persona.id'), nullable = False)
    persona = db.relationship('Persona', back_populates='producto', lazy=True)
    # Relación uno a muchos con Lote
    id_lote = db.Column(db.Integer, db.ForeignKey('lote.id'), nullable = False)
    lote = db.relationship('Lote', back_populates='producto', lazy=True)
    
    def serialize(self):
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
        }