from app import db
from models.estadoPr import EstadoPr
import uuid

class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    nombrePr = db.Column(db.String(100))
    fechaPr = db.Column(db.Date)
    fechaVen=db.Column(db.Date)
    cantidadL = db.Column(db.Integer)
    estadoPr = db.Column(db.Enum(EstadoPr), nullable = False,default='Buen_Estado')
    imagen = db.Column(db.String(250), nullable=True)
    # Relación uno a muchos con Producto
    producto = db.relationship('Producto', back_populates='lote', lazy=True)
    
    id_sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable = False)
    sucursal = db.relationship('Sucursal', backref='sucursal', lazy=True)
    
    
    #@property
    def serialize(self):
        return {
            'nombrePr': self.nombrePr,
            'fechaPr': self.fechaPr.isoformat() if self.fechaPr else None,
            'fechaVen': self.fechaVen.isoformat() if self.fechaVen else None,
            'cantidadL': self.cantidadL,
            'estadoPr': self.estadoPr.value,
            'imagen': self.imagen if self.imagen else 'No tiene imagen',
            'external_id':self.external_id
            
        }
        
