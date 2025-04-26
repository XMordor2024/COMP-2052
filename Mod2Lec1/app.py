from flask import Flask, render_template

app = Flask(__name__)

# Datos Dinámicos
juegos = [
    {"id": 1, "nombre": "Final Fantasy 7 Rebirth", "precio": 69.99},
    {"id": 2, "nombre": "Stellar Blade", "precio": 70.00}
]

usuarios = [
    {"id": 1, "nombre": "Andres", "rol": "Usuario"},
    {"id": 2, "nombre": "Maria", "rol": "Usuario"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/juegos")
def mostrar_productos():
    return render_template("juegos.html", juegos=juegos)

@app.route("/usuarios")
def mostrar_usuarios():
    return render_template("usuarios.html", usuarios=usuarios)

if __name__ == "__main__":
    app.run(debug=True)