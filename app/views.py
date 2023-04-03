from flask import render_template, jsonify, request
from app import app, db
from app.models import Usuario, Proyecto, Institucion
from datetime import date, datetime


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/generar_datos')
def test_data():

    institucion_1 = Institucion(nombre='Universidad de Santiago de Chile', descripcion='Universidad pública en la Región Metropolitana', direccion='Av. Libertador Bernardo O\'Higgins 3363, Estación Central', fecha_creacion=date(1849, 4, 19))
    institucion_2 = Institucion(nombre='Universidad Católica de Chile', descripcion='Universidad privada en la Región Metropolitana', direccion='Av. Libertador Bernardo O\'Higgins 340, Santiago', fecha_creacion=date(1888, 6, 21))
    institucion_3 = Institucion(nombre='Pontificia Universidad Católica de Valparaíso', descripcion='Universidad privada en la Región de Valparaíso', direccion='Av. Brasil 2950, Valparaíso', fecha_creacion=date(1928, 6, 11))

    db.session.add_all([institucion_1, institucion_2, institucion_3])
    db.session.commit()

    usuario_1 = Usuario(nombre='Juan', apellidos='Pérez García', rut='123456789-0', fecha_nacimiento='1990-05-12', cargo='Ingeniero', edad=33)
    usuario_2 = Usuario(nombre='María', apellidos='López Ramírez', rut='987654321-0', fecha_nacimiento='1995-10-18', cargo='Analista', edad=28)
    usuario_3 = Usuario(nombre='Pedro', apellidos='González Torres', rut='456789123-0', fecha_nacimiento='1985-02-28', cargo='Gerente', edad=38)

    db.session.add_all([usuario_1, usuario_2, usuario_3])
    db.session.commit()

    proyecto1 = Proyecto(nombre="Proyecto A", descripcion="Descripción del proyecto A", fecha_inicio=date(2022, 1, 1), fecha_termino=date(2022, 6, 30), institucion_id= institucion_1.id, usuario_id= usuario_1.id)
    proyecto2 = Proyecto(nombre="Proyecto B", descripcion="Descripción del proyecto B", fecha_inicio=date(2022, 2, 1), fecha_termino=date(2022, 7, 31), institucion_id= institucion_1.id, usuario_id= usuario_2.id)
    proyecto3 = Proyecto(nombre="Proyecto C", descripcion="Descripción del proyecto C", fecha_inicio=date(2022, 3, 1), fecha_termino=date(2022, 8, 31), institucion_id= institucion_1.id, usuario_id= usuario_2.id)
    proyecto4 = Proyecto(nombre="Proyecto D", descripcion="Descripción del proyecto D", fecha_inicio=date(2022, 4, 1), fecha_termino=date(2022, 9, 30), institucion_id= institucion_2.id, usuario_id= usuario_3.id)
    proyecto5 = Proyecto(nombre="Proyecto E", descripcion="Descripción del proyecto E", fecha_inicio=date(2022, 5, 1), fecha_termino=date(2022, 10, 31), institucion_id= institucion_2.id, usuario_id= usuario_1.id)
    proyecto6 = Proyecto(nombre="Proyecto F", descripcion="Descripción del proyecto F", fecha_inicio=date(2022, 6, 1), fecha_termino=date(2022, 11, 30), institucion_id= institucion_3.id, usuario_id= usuario_3.id)
    proyecto7 = Proyecto(nombre="Proyecto G", descripcion="Descripción del proyecto G", fecha_inicio=date(2022, 7, 1), fecha_termino=date(2022, 12, 31), institucion_id= institucion_3.id, usuario_id= usuario_1.id)
    proyecto8 = Proyecto(nombre="Proyecto H", descripcion="Descripción del proyecto H", fecha_inicio=date(2022, 8, 1), fecha_termino=date(2023, 1, 31), institucion_id= institucion_3.id, usuario_id= usuario_2.id)

    db.session.add_all([proyecto1, proyecto2, proyecto3, proyecto4, proyecto5, proyecto6, proyecto7, proyecto8])
    db.session.commit()

    return render_template('index.html')

## SERVICIOS DE LA API ##
@app.route('/api/instituciones', methods=['GET'])
def get_instituciones():
    instituciones = Institucion.query.all()

    return jsonify([i.to_dict() for i in instituciones])

## CRUD INSTITUCIONES ##

@app.route('/api/instituciones/<id>', methods=['GET'])
def get_institucion(id):

    institucion = Institucion.query.filter_by(id = id).first()

    if institucion is None:
        return jsonify({'error': 'Institución no se encuentra.'})

    proyectos = institucion.get_proyectos()

    return jsonify(proyectos)

@app.route('/api/instituciones', methods=['POST'])
def create_instituciones():

    nueva_institucion = Institucion(nombre=request.json['nombre'], descripcion=request.json['descripcion'], direccion=request.json['direccion'], fecha_creacion=request.json['fecha_creacion'])
    print(nueva_institucion)
    db.session.add(nueva_institucion)
    db.session.commit()

    return jsonify(nueva_institucion.to_dict()), 201

@app.route('/api/instituciones/<id>', methods=['PUT'])
def update_institucion(id):

    institucion = Institucion.query.filter_by(id = id).first()
    
    if institucion is None:
        return jsonify({'error': 'Institución no se encuentra.'})

    fecha_creacion_str = request.json.get('fecha_creacion', institucion.fecha_creacion)

    institucion.nombre = request.json.get('nombre', institucion.nombre)
    institucion.descripcion = request.json.get('descripcion', institucion.descripcion)
    institucion.direccion = request.json.get('direccion', institucion.direccion)
    institucion.fecha_creacion = datetime.strptime(fecha_creacion_str, '%Y-%m-%d')
    return jsonify(institucion.to_dict()), 201

@app.route('/api/instituciones/<id>', methods=['DELETE'])
def delete_institucion(id):

    institucion = Institucion.query.filter_by(id = id).first()

    if institucion is None:
        return jsonify({'error': 'No se encuentra institución solicitada.'})

    proyectos = Proyecto.query.filter_by(institucion_id = id).all()

    if proyectos is not None:
        for proyecto in proyectos:
            db.session.delete(proyecto)
        db.session.commit()

    db.session.delete(institucion)
    db.session.commit()

    return jsonify({'respuesta':'Institución eliminada correctamente.'})

@app.route('/api/proyectos', methods=['GET'])
def get_proyectos():

    proyectos = Proyecto.query.all()

    return jsonify([i.to_dict() for i in proyectos])

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():

    usuarios = Usuario.query.all()

    return jsonify([i.to_dict() for i in usuarios])

@app.route('/api/usuarios/<rut>', methods=['GET'])
def get_usuario(rut):

    usuario = Usuario.query.filter_by(rut = rut).first()

    if usuario is None:
        return jsonify({'error': 'No se encuentra usuario solicitado.'})

    return jsonify(usuario.get_proyectos())

@app.route('/api/proyectos/tiempo_finalizacion/', methods=['GET'])
def get_tiempo_proyectos():

    proyectos = Proyecto.query.filter(Proyecto.fecha_inicio < Proyecto.fecha_termino).all()

    return jsonify([i.to_dict_days_until_end() for i in proyectos])