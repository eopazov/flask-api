from app import db
import unicodedata
import datetime

class Institucion(db.Model):

    __tablename__ = 'instituciones'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    fecha_creacion = db.Column(db.Date)
    

    def to_dict(self):

        ubicacion = ''.join(c for c in unicodedata.normalize('NFKD', self.direccion) if not unicodedata.combining(c))

        data = {
            'id': self.id,
            'nombre': self.nombre,
            'abreviacion': self.nombre[:3].upper(),
            'descripcion': self.descripcion,
            'direccion': self.direccion,
            'fecha_creacion' : self.fecha_creacion.strftime("%d/%m/%Y"),
            'ubicacion': "https://www.google.com/maps/search/"+ ubicacion.replace(" ", "+")
        }

        return data
    
    def get_proyectos(self):

        proyectos = Proyecto.query.filter_by(institucion_id = self.id).all()

        data_proyectos = []
        
        for proyecto in proyectos:
            data_proyectos.append(proyecto.to_dict_with_user())

        ubicacion = ''.join(c for c in unicodedata.normalize('NFKD', self.direccion) if not unicodedata.combining(c))

        data = {
            'id': self.id,
            'nombre': self.nombre,
            'abreviacion': self.nombre[:3].upper(),
            'descripcion': self.descripcion,
            'direccion': self.direccion,
            'fecha_creacion' : self.fecha_creacion.strftime("%d/%m/%Y"),
            'ubicacion': "https://www.google.com/maps/search/"+ ubicacion.replace(" ", "+"),
            'proyectos': data_proyectos
        }

        return data

class Usuario(db.Model):

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    cargo = db.Column(db.String(50))
    edad = db.Column(db.Integer)

    def to_dict(self):
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'rut': self.rut,
            'fecha_nacimiento': self.fecha_nacimiento.strftime("%d/%m/%Y"),
            'cargo': self.cargo,
            'edad': self.edad
        }

        return data

    def get_proyectos(self):

        proyectos = Proyecto.query.filter_by(usuario_id = self.id).all()

        data_proyectos = []

        for proyecto in proyectos:
            new_dict = proyecto.to_dict()
            new_dict.pop('usuario_id')

            data_proyectos.append(new_dict)

        data = {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'rut': self.rut,
            'fecha_nacimiento': self.fecha_nacimiento.strftime("%d/%m/%Y"),
            'cargo': self.cargo,
            'edad': self.edad,
            'proyectos_a_cargo' : data_proyectos
        }

        return data

class Proyecto(db.Model):

    __tablename__ = 'proyectos'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_termino = db.Column(db.Date)
    institucion_id = db.Column(db.Integer, db.ForeignKey('instituciones.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.strftime("%d/%m/%Y"),
            'fecha_termino': self.fecha_termino.strftime("%d/%m/%Y"),
            'institucion_id': self.institucion_id,
            'usuario_id': self.usuario_id,
            'dias_para_termino' : ( self.fecha_termino - self.fecha_inicio).days
        }

        return data
    
    def to_dict_days_until_end(self):
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'dias_para_termino' : ( self.fecha_termino - self.fecha_inicio).days
        }

        return data

    def to_dict_with_user(self):

        user = Usuario.query.filter_by(id = self.usuario_id).first()

        data = {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.strftime("%d/%m/%Y"),
            'fecha_termino': self.fecha_termino.strftime("%d/%m/%Y"),
            'usuario_responsable': user.to_dict()
        }

        return data
