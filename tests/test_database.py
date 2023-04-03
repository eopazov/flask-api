import pytest
from app import db
from flask import Flask
from datetime import date
from app.models import Institucion, Proyecto, Usuario

@pytest.fixture
def test_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/test_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    yield app.test_client()
    db.drop_all()

@pytest.fixture
def institucion():
    institucion = Institucion(
        nombre='Institucion de Prueba',
        descripcion='Esta es una institucion de prueba',
        direccion='Calle de Prueba 123',
        fecha_creacion= date.today()
    )
    db.session.add(institucion)
    db.session.commit()
    return institucion

@pytest.fixture
def usuario():
    usuario = Usuario(
        nombre='Usuario',
        apellidos='De Prueba',
        rut='12345678-9',
        fecha_nacimiento=date.today(),
        cargo='Desarrollador',
        edad=25
    )
    db.session.add(usuario)
    db.session.commit()
    return usuario

@pytest.fixture
def proyecto(institucion, usuario):
    proyecto = Proyecto(
        nombre='Proyecto de Prueba',
        descripcion='Este es un proyecto de prueba',
        fecha_inicio=date.today(),
        fecha_termino=date.today(),
        institucion_id=institucion.id,
        usuario_id=usuario.id
    )
    db.session.add(proyecto)
    db.session.commit()
    return proyecto

def test_institucion_add(institucion):
    assert institucion.nombre == 'Institucion de Prueba'
    assert institucion.descripcion == 'Esta es una institucion de prueba'
    assert institucion.direccion == 'Calle de Prueba 123'
    assert institucion.fecha_creacion == date.today()

def test_usuario_add(usuario):
    assert usuario.nombre == 'Usuario'
    assert usuario.apellidos == 'De Prueba'
    assert usuario.rut == '12345678-9'
    assert usuario.fecha_nacimiento == date.today()
    assert usuario.cargo == 'Desarrollador'
    assert usuario.edad == 25

def test_proyecto_add(proyecto, institucion, usuario):
    assert proyecto.nombre == 'Proyecto de Prueba'
    assert proyecto.descripcion == 'Este es un proyecto de prueba'
    assert proyecto.fecha_inicio == date.today()
    assert proyecto.fecha_termino == date.today()
    assert proyecto.institucion_id == institucion.id
    assert proyecto.usuario_id == usuario.id