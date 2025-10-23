# backend_file/src/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

# Tabla intermedia para relación muchos a muchos
proyecto_hashtag = db.Table(
    'proyecto_hashtag',
    db.Column('proyecto_id', db.Integer, db.ForeignKey('proyecto.id', ondelete='CASCADE'), primary_key=True),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id', ondelete='CASCADE'), primary_key=True)
)

class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Proyecto(db.Model):
    __tablename__ = 'proyecto'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    breve_descripcion = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)  # HTML
    analisis = db.Column(db.Text, nullable=False)     # HTML
    categoria = db.Column(db.String(50), nullable=False)
    enlace_documentos = db.Column(db.String(500))
    enlace_herramienta = db.Column(db.String(500))
    enlace_github = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    hashtags = db.relationship('Hashtag', secondary=proyecto_hashtag, back_populates='proyectos')
    medios = db.relationship('Medio', back_populates='proyecto', cascade='all, delete-orphan')

class Hashtag(db.Model):
    __tablename__ = 'hashtag'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    proyectos = db.relationship('Proyecto', secondary=proyecto_hashtag, back_populates='hashtags')

class Medio(db.Model):
    __tablename__ = 'medio'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'imagen' o 'video'
    orden = db.Column(db.Integer, nullable=False, default=0)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id', ondelete='CASCADE'), nullable=False)
    proyecto = db.relationship('Proyecto', back_populates='medios')