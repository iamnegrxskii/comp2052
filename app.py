from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "nombre_app": "Actividad Modulo 1 Leccion 2 del curso Comp 2052.",
        "version": "1.0",
        "descripcion": "Este servidor tiene dos rutas: /info y /mensaje."
    })

# Ruta POST /mensaje
@app.route('/mensaje', methods=['POST'])
def mensaje():
    datos = request.get_json()
    if not datos or 'mensaje' not in datos:
        return jsonify({"error": "Falta el campo 'mensaje' en el cuerpo JSON"}), 400
    mensaje_recibido = datos['mensaje']
    respuesta = f"{mensaje_recibido}."
    return jsonify({"respuesta": respuesta})

# Ejecución del servidor
if __name__ == '__main__':
    app.run(debug=True)