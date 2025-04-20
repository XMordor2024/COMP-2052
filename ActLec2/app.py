from flask import Flask, request, jsonify

app = Flask (__name__)

mensajes = ["Hola", "Como estas?"]

@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        'version de prueba': "2.0",
        'usuario': 'Ezequiel D. Figueroa Rosario'
    })

@app.route("/mensaje", methods=["GET","POST"])
def mensaje():
    if request.method == "GET":
        return jsonify({"mensajes": mensajes})

    if request.method == "POST":
        data = request.json
        if not data or "mensaje" not in data:
            return jsonify({"error": "Falta el campo mensajes"}), 400

    
        mensajes.append(data["mensaje"])
        return jsonify ({"respuesta": f"Mensaje recibido: '{data['mensaje']}'"}), 201

if __name__ == '__main__':
    app.run(debug=True)