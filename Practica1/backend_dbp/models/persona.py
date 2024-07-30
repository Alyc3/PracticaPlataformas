from app import db
import uuid
from datetime import datetime


class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    identificacion = db.Column(db.String(20))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # Relación uno a muchos con Censo_Persona
    producto = db.relationship('Producto', back_populates='persona', lazy=True)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable = False)
    cuenta = db.relationship('Cuenta', back_populates='persona', lazy=True)

    # Getters and setters
    @property
    def apellido(self):
        return self.apellidos

    @apellido.setter
    def apellido(self, value):
        self.apellidos = value

    @property
    def nombre(self):
        return self.nombres

    @nombre.setter
    def nombre(self, value):
        self.nombres = value
    
    def serialize(self):
        return {
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'identificacion': self.identificacion,
            'cuenta': [cuenta.serialize() for cuenta in self.cuenta if cuenta.estado == 1],
        }
    
    def copy(self):
        new_persona = Persona(
            id=self.id,
            nombres=self.nombres,
            apellidos=self.apellidos,
            direccion=self.direccion,
            telefono=self.telefono,
            identificacion=self.identificacion,
            external_id=self.external_id
        )
        return new_persona
        