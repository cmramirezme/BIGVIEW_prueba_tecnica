from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Configuración de la base de datos
mongo = MongoClient("mongodb://user-management-db:27017/")
db = mongo["UsersDB"]
users_collection = db["Users"]

# Configuración del secreto para los tokens JWT
app.config["SECRET_KEY"] = "your_secret_key"

# Ruta para registro de usuarios
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Verificar si el usuario ya existe
        if db.Users.find_one({"username": username}):
            return jsonify({"message": "El usuario ya está registrado."}), 409


        # Crear el usuario en la base de datos
        db.Users.insert_one({
            "username": username,
            "password": password
        })

        return jsonify({"message": "Usuario registrado exitosamente."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para login de usuarios
@app.route('/login', methods=['GET'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Buscar el usuario en la base de datos
        user = db.Users.find_one({"username": username})
        if not user:
            return jsonify({"message": "Usuario no encontrado."}), 404

        # Verificar la contraseña
        if user["password"]!= password:
            return jsonify({"message": "Contraseña incorrecta."+user["password"]+password}), 401

        # Generar un token JWT
        token = jwt.encode({
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config["SECRET_KEY"], algorithm="HS256")

        return jsonify({"message": "Inicio de sesión exitoso.", "token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""# Ruta para verificar el token (opcional, puede ser usada como middleware)
@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token no proporcionado."}), 401

        # Decodificar el token
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return jsonify({"message": "Token válido.", "data": decoded}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "El token ha expirado."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido."}), 401"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
