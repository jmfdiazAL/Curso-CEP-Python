# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabla para almacenar la versión de la base de datos
class DatabaseVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(10), nullable=False, default='1.0')

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))  # URL de la imagen
    visibilidad = db.Column(db.String(20), nullable=False, default='publica')  # publica, privada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    contador_favoritos = db.Column(db.Integer, default=0)
    usuario = db.relationship('Usuario', backref='listas')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    enlace = db.Column(db.String(200))
    imagen = db.Column(db.String(200))
    orden = db.Column(db.Integer, default=0)
    lista = db.relationship('Lista', backref='items')

class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class ListaEtiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey('etiqueta.id'), nullable=False)

class ItemEtiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    id_etiqueta = db.Column(db.Integer, db.ForeignKey('etiqueta.id'), nullable=False)

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)

class Suscripcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'))
    id_item = db.Column(db.Integer, db.ForeignKey('item.id'))
    fecha_like = db.Column(db.DateTime, default=datetime.utcnow)

class Checked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    fecha_checked = db.Column(db.DateTime, default=datetime.utcnow)