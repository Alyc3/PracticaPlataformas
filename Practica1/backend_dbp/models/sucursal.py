from app import db
import uuid
from datetime import datetime

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def serialize(self):
        return {
            'nombre': self.nombre,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'id': self.id,
            'external_id': self.external_id
        }
    
    
    def copy_data(self, value):
        self.nombre = value.get('nombre')
        self.latitud = value.get('latitud')
        self.longitud = value.get('longitud')
        self.id = value.get('id')
        self.external_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return self