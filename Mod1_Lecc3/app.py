from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacén de usuarios en memoria
usuarios = []

@app.route("/info", methods=["GET"])
def info():
    sistema_info = {
        "nombre": "Sistema de Gestion",
        "version": "1.0",
        "descripcion": "Este sistema gestiona usuarios y productos.",
    }
    return jsonify(sistema_info)

@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    data = request.json
    nombre = data.get("nombre")
    correo = data.get("correo")
    
    if not nombre or not correo:
        return jsonify({"error": "Ambos campos, 'nombre' y 'correo', son obligatorios."}), 400

    usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(usuario)
    return jsonify({"mensaje": "Usuario creado exitosamente.", "usuario": usuario})

@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    if not usuarios:
        return jsonify({"mensaje": "No hay usuarios registrados por el momento."})
    return jsonify({"usuarios": usuarios})

if __name__ == "__main__":
    app.run(debug=True)