# Prueba tecnica Restful API en Flask
***
Desarrollo de una prueba técnica en Python, desarrollando una Restful API en Flask, usando base de datos PostgreSQL.

## Aplicacion

### Views

    index(): Establece un menú simple para navegar por los apartados solicitados en la API.
    test_data(): Genera datos en la base de datos, necesarios para realizar pruebas de la aplicación.

    Instituciones
        Se crea el CRUD completo de estas para funcionar en la API.
    Usuarios
        Se listan todos los usuarios y también se puede acceder por rut a uno de ellos.
    Proyectos
        Se pueden listar todos los proyectos y también listar sólo el nombre y el tiempo con el que va a terminar.

### Models

    Institucion
    Proyecto
    Usuario

    Se añaden las funciones to_dict() para poder realizar las vistas de la API.

### Tests

    Se realizan pruebas en la creación de objetos de models.

### Docs

    Se entrega una documentación en Swagger del proyecto.

### POSTMAN json

    Se da entrega de un archivo llamado 'Prueba tecnica EO.postman_collection.json' para ser cargado en Postman, contiene las pruebas realizadas de la API.