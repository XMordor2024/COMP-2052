from flask import Flask, render_template

app = Flask(__name__)

# Datos Dinámicos
productos = [
    {"id": 1, "nombre": "uva", "precio": 15},
    {"id": 2, "nombre": "naranja", "precio": 15}
]

usuarios = [
    {"id": 1, "nombre": "Andres", "posicion": "Retailer"},
    {"id": 2, "nombre": "Maria", "posicion": "Usuario"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos")
def mostrar_productos():
    return render_template("productos.html", productos=productos)

@app.route("/usuarios")
def mostrar_usuarios():
    return render_template("usuarios.html", usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)