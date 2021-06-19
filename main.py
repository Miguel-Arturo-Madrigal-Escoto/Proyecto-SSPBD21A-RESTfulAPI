from flask import Flask, request, jsonify
from conexion import *

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route("/api/v1/usuarios", methods=["POST", "GET"])
    def usuario(id=None):
        if request.method == "POST" and request.is_json:
            try:
                info_user = request.get_json()
                correo = info_user['correo']
                contrasena = info_user['contrasena']

                if crear_usuario(correo, contrasena):
                    return jsonify({"code": "ok"})
                else:
                    return jsonify({"code": "ya existe"})
            except:
                return jsonify({"code": "error"})
        elif request.method == "GET" and id is None:
            return jsonify(get_usuarios())
        
    @app.route("/api/v1/albums", methods=["POST", "GET"])
    @app.route("/api/v1/albums/<int:id>", methods=["DELETE", "PATCH"])
    def album(id=None):
        if request.method == "POST" and request.is_json:
            data = request.get_json()
            titulo = data['titulo']
            anio_produccion = data['anio_produccion']
            caratula = data['caratula']
            usuarioID = data['usuarioID']
            artistaID = data['artistaID']

            try:
                if insertar_album(titulo, anio_produccion, caratula, usuarioID, artistaID):
                    return jsonify({"code": "ok"})
                else:
                    return jsonify({"code": "album existente"})
            except:
                return jsonify({"code": "error"})

        elif request.method == "GET":
            return jsonify(get_albums())
        elif request.method == "DELETE" and id is not None:
            return jsonify({"code": "album eliminado"}) if eliminar_album(id) > 0 else jsonify({"code": "error"})
        elif request.method == "PATCH" and id is not None and request.is_json:
            data = request.get_json()
            columna = data['columna']
            valor = data['valor']

            try:
                return jsonify({"code": "album modificado"}) if modificar_album(id, columna, valor) else jsonify({"code": "album no modificado"})
            except:
                return jsonify({"code": "error"})
        
    @app.route("/api/v1/artistas", methods=["POST", "GET"])
    def artista():
        if request.method == "POST" and request.is_json:
            info_artist = request.get_json()  
            nombre = info_artist['nombre']
            fotografia = info_artist['fotografia']
            biografia = info_artist['biografia']

            try:
                return jsonify({"code": "ok"}) if insertar_artista(nombre, fotografia, biografia) else jsonify({"code": "artista existente"})
            except:
                return jsonify({"code": "error"})
        elif request.method == "GET":
            return jsonify(get_artistas())
    
    @app.route("/api/v1/sesiones", methods=["POST"])
    def sesion():
        if request.method == "POST" and request.is_json:
            try:git status
                data = request.get_json()
                correo = data['correo']
                contrasena = data['contrasena']

                id, ok = iniciar_sesion(correo, contrasena)

                return jsonify({"code": "ok", "id": id}) if ok else jsonify({"code": "no existe"})
            
            except:
                return jsonify({"code":"error"})
    
    @app.route("/api/v1/tracks", methods=["POST", "GET"])
    @app.route("/api/v1/tracks/<int:id>/album", methods=["GET"])
    def track(id=None):
        if request.method == "POST" and request.is_json:
            try:
                data = request.get_json()
                titulo = data['titulo']
                duracion = data['duracion']
                albumID = data['albumID']

                return jsonify({"code": "ok"}) if insertar_track(titulo,duracion,albumID) else jsonify({"code": "track existente"})
            except:
                return jsonify({"code": "error"})

        elif request.method == "GET" and id is None:
            return jsonify(get_tracks())
        
        elif request.method == "GET" and id is not None:
            return jsonify(get_tracks_album(id))
    
    @app.route("/api/v1/resenias", methods=["POST", "GET"])
    def resenias():
        if request.method == "POST" and request.is_json:
            try:
                data = request.get_json()
                comentario = data['comentario']
                usuarioID = data['usuarioID']
                albumID = data['albumID']

                return jsonify({"code": "ok"}) if insertar_resenia(comentario, usuarioID, albumID) else jsonify({"code": "error"})
            except:
                return jsonify({"code": "error"})

        elif request.method == "GET":
            return jsonify(get_resenias())

    @app.route("/api/v1/fotografias", methods=["GET"])   
    def fotografias():
        if request.method == "GET":
            return jsonify(get_fotografias())

    app.run(debug=True)
