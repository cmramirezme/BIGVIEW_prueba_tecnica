from flask import Flask, request, jsonify, redirect
import requests
import jwt

app = Flask(__name__)

# Configuración de microservicios
MICROSERVICES = {
    "user_service": "http://user-management:5003",  # Dirección del microservicio de gestión de usuarios
    "flights-management": "http://flight-search:5001",  # Dirección del microservicio de reservas
}

# Ruta general para manejar solicitudes al microservicio de reservas
@app.route('/flights-management/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def booking_service(path):
    """Verifica la autenticación y redirige a 'user_service' si es inválida."""
    token = request.headers.get('Authorization')  # Obtener el token de autenticación

    # Verificar si el token está presente y válido
    if not token or not validate_token(token):
        # Si no hay token o es inválido, redirige al microservicio de gestión de usuarios
        return redirect_to_user_management()

    # Si el token es válido, reenvía la solicitud al microservicio de reservas
    url = f"{MICROSERVICES['flights-management']}/{path}"
    response = forward_request(url)
    return response


# Ruta general para manejar solicitudes al microservicio de gestion de usuarios
@app.route('/user-management/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_management(path):
    url = f"{MICROSERVICES['user_service']}/{path}"
    response = forward_request(url)
    return response

def validate_token(token):
    """Valida el token proporcionado y retorna True si es válido."""
    try:
        # Decodificar el token usando el secreto y el algoritmo especificado
        decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])

        # Puedes agregar más validaciones si es necesario, por ejemplo:
        # Verificar si el token contiene campos requeridos como 'username'
        if "username" in decoded_token and "exp" in decoded_token:
            return True  # Token válido

        return False  # Token inválido si faltan campos importantes

    except jwt.ExpiredSignatureError:
        # El token expiró
        return False
    except jwt.InvalidTokenError:
        # El token es inválido
        return False


def redirect_to_user_management():
    """Indica al usuario las URL para registro o inicio de sesión en el microservicio user-management."""
    return jsonify({
        "message": "Token inválido o no proporcionado. Por favor, utiliza una de las siguientes URLs:",
        "login_url": "http://localhost:5000/user-management/login",  # Para iniciar sesión
        "register_url": "http://localhost:5000/user-management/register"  # Para crear un nuevo usuario
    }), 401  # Código 401 indica que la autenticación es requerida


def forward_request(url):
    """Redirige la solicitud HTTP al microservicio correspondiente."""
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            json=request.get_json(silent=True),
            params=request.args
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
