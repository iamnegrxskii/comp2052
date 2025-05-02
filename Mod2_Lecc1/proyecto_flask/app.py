from flask import Flask, render_template

app = Flask(__name__)

# Datos dinámicos
productos = ["Laptop", "Ratón", "Teclado", "Monitor"]
usuarios = [
    {"nombre": "Juan Pérez", "correo": "juan.perez@example.com"},
    {"nombre": "Ana García", "correo": "ana.garcia@example.com"}
]

@app.route('/')
def inicio():
    return render_template("base.html", titulo="Inicio")

@app.route('/pagina1')
def pagina1():
    return render_template("pagina1.html", titulo="Página 1", productos=productos)

@app.route('/pagina2')
def pagina2():
    usuarios = [
        {"nombre": "Juan Pérez", "correo": "juan.perez@example.com"},
        {"nombre": "Ana García", "correo": "ana.garcia@example.com"}
    ]
    return render_template("pagina2.html", titulo="Página 2", usuarios=usuarios)


if __name__ == '__main__':
    app.run(debug=True)