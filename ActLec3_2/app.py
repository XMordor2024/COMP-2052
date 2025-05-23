from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenamiento en memoria
usuarios = [{
    "usuarios":[
    {
    "id": 1,
    "nombre": "Juan Perez",
    "correo": "juan@ejemplo.com",
    "fecha_registro": "20-04-2025",
    "Productos_comprados": "101"
    },
    {
    "id": 2,
    "nombre": "Diego Cabrera",
    "correo": "diego@ejemplar.com",
    "fecha_registro": "10-05-2025",
    "Productos_comprados": "102"
    }
    ]
}]

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "app": "Gestión de Usuarios y Productos",
        "version": "1.0",
        "status": "activo"
    })

# Ruta POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre or not correo:
        return jsonify({
            "error": "Faltan datos requeridos. Se necesita 'nombre' y 'correo'."
        }), 400

    nuevo_usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(nuevo_usuario)
    return jsonify({
        "mensaje": "Usuario creado exitosamente.",
        "usuario": nuevo_usuario
    }), 201

# Ruta GET /usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(usuarios), 200

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
