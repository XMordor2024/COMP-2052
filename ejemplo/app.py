from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hola Mundo!</h1>"

@app.route("/adios")
def hello_world():
    return "Adios Mundo!"

if __name__ == "__main__":
    app.run(debug=True)