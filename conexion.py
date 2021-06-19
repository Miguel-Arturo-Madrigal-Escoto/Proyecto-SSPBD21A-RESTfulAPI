from datetime import datetime
import mysql.connector
import hashlib

db = mysql.connector.connect(
    user = 'MiguelMadrigal',
    password = 'admin1234',
    database = 'misdiscos'
)

cursor = db.cursor()

def get_usuarios():
    query = 'SELECT * FROM usuario'
    cursor.execute(query)

    usuarios = []
    for row in cursor.fetchall():
        usuario = {
            "id": row[0],
            "correo": row[1],
            "contrasena": row[2]
        }
        usuarios.append(usuario)
    
    return usuarios

def existe_usuario(correo):
    query = 'SELECT COUNT(*) FROM usuario WHERE correo = %s'
    cursor.execute(query, (correo,))

    return cursor.fetchone()[0] == 1

def crear_usuario(correo, contrasena):
    if existe_usuario(correo):
        return False
    else:
        h_pass = hashlib.new('sha256', bytes(contrasena, 'utf-8'))
        h_pass = h_pass.hexdigest()
        sql = 'INSERT INTO usuario (correo, contrasena) VALUES (%s,%s)'
        cursor.execute(sql, (correo, h_pass))
        db.commit()

        return cursor.rowcount

fotografias = {}
def get_albums():
    query = 'SELECT * FROM album'
    cursor.execute(query)

    albums = []
    for row in cursor.fetchall():
        album = {
            "id": row[0],
            "titulo": row[1],
            "anio_produccion": row[2],
            "caratula": row[3],
            "usuarioID": row[4]         
        }

        # * getArtistasAlbum
        sql = 'SELECT artistaID FROM pertenece WHERE albumID = %s'
        cursor.execute(sql, (album['id'],))

        artistasID = [k[0] for k in cursor.fetchall()]
        artistas = []
        for row in artistasID:
            get_nombres = 'SELECT nombre, fotografia FROM artista WHERE id = %s'
            cursor.execute(get_nombres, (row,))
            artista = cursor.fetchone()
            artistas.append(artista[0])
            fotografias[artista[0].replace(' ','')] = artista[1]
        
        album['nombre_artistas'] = artistas
        albums.append(album)
    
    return albums

def get_tracks_album(id):
    query = 'SELECT * FROM track WHERE albumID = %s'
    cursor.execute(query, (id,))

    tracks = []

    for row in cursor.fetchall():
        track = {
            'id': row[0],
            'titulo': row[1],
            'duracion': row[2],
            'albumID': row[3]
        }
        tracks.append(track)
    
    return tracks


def get_fotografias():
    return fotografias

def existe_album(titulo, anio_produccion, usuarioID, artistaID):
    query_cont = 'SELECT COUNT(*) FROM album WHERE titulo = %s AND anio_produccion = %s AND usuarioID = %s'
    cursor.execute(query_cont, (titulo, anio_produccion, usuarioID))

    cont = cursor.fetchone()[0]
    if cont > 0:
        query = 'SELECT id FROM album WHERE titulo = %s AND anio_produccion = %s AND usuarioID = %s'
        cursor.execute(query, (titulo, anio_produccion, usuarioID))

        albumID = cursor.fetchone()[0]
        query_produce = 'SELECT * FROM pertenece WHERE albumID = %s'
        cursor.execute(query_produce, (albumID,))

        album_artista = (albumID, artistaID)
        pertence = cursor.fetchall()
        if album_artista not in pertence:
            return albumID
        else:
            return 0
    else:
        return -1

def insertar_album(titulo, anio_produccion, caratula, usuarioID, artistaID):
    code = existe_album(titulo, anio_produccion, usuarioID, artistaID)
    if code == 0:
        return False
    elif code == -1:
        sql = 'INSERT INTO album (titulo, anio_produccion, caratula, usuarioID) VALUES (%s,%s,%s,%s)'
        cursor.execute(sql, (titulo, anio_produccion, caratula, usuarioID))
        db.commit()
 
        albumID = cursor.lastrowid  
        sql_pertenece = 'INSERT INTO pertenece (albumID, artistaID) VALUES (%s,%s)'
        cursor.execute(sql_pertenece, (albumID, artistaID))
        db.commit()
        
        return cursor.rowcount

    else:
        sql_pertenece = 'INSERT INTO pertenece (albumID, artistaID) VALUES (%s,%s)'
        cursor.execute(sql_pertenece, (albumID:=code, artistaID))
        db.commit()
        
        return cursor.rowcount

def existe_artista(nombre):
    query = 'SELECT COUNT(*) FROM artista WHERE nombre = %s'
    cursor.execute(query, (nombre,))

    return cursor.fetchone()[0]

def insertar_artista(nombre, fotografia, biografia):
    if existe_artista(nombre):
        return False
    else:
        sql = 'INSERT INTO artista (nombre, fotografia, biografia) VALUES (%s,%s,%s)'
        cursor.execute(sql, (nombre, fotografia, biografia))
        db.commit()

        return cursor.rowcount

def get_artistas():
    query = 'SELECT * FROM artista'
    cursor.execute(query)

    artistas = []
    for row in cursor.fetchall():
        artista = {
            "id": row[0],
            "nombre": row[1],
            "fotografia": row[2],
            "biografia": row[3]
        }
        artistas.append(artista)
    
    return artistas

def iniciar_sesion(correo, contrasena):
    h_pass = hashlib.new('sha256', bytes(contrasena, 'utf-8'))
    h_pass = h_pass.hexdigest()

    sql = 'SELECT id FROM usuario WHERE correo = %s AND contrasena = %s'
    cursor.execute(sql, (correo, h_pass))

    id = cursor.fetchone()

    return (id[0], True) if id else (None, False)

def eliminar_album(id):  
    sql = 'DELETE FROM pertenece WHERE albumID = %s'
    cursor.execute(sql, (id,))
    db.commit()

    if cursor.rowcount > 0:
        sql = 'DELETE FROM resenia WHERE albumID = %s'
        cursor.execute(sql, (id,))
        db.commit()

        sql = 'DELETE FROM track WHERE albumID = %s'
        cursor.execute(sql, (id,))
        db.commit()

        sql = 'DELETE FROM album WHERE id = %s'
        cursor.execute(sql, (id,))
        db.commit()
        
    return cursor.rowcount

def modificar_album(id, columna, valor):
    update = f'UPDATE album SET {columna} = %s WHERE id = %s'
    cursor.execute(update, (valor, id))
    db.commit()

    return cursor.rowcount

def existe_track(titulo, albumID):
    
    query = 'SELECT COUNT(*) FROM track WHERE titulo = %s AND albumID = %s'
    cursor.execute(query, (titulo, albumID))
    
    return cursor.fetchone()[0]

def insertar_track(titulo, duracion, albumID):
    if existe_track(titulo, albumID):
        return False
    else:
        sql = 'INSERT INTO track (titulo, duracion, albumID) VALUES(%s,%s,%s)'
        cursor.execute(sql, (titulo,duracion,albumID))
        db.commit()

    return cursor.rowcount

def get_tracks():
    query = 'SELECT id, titulo, duracion FROM track'
    cursor.execute(query)

    tracks = []
    for row in cursor.fetchall():
        track = {
            "id": row[0],
            "titulo": row[1],
            "duracion": row[2]
        }
        tracks.append(track)
    
    return tracks

def insertar_resenia(comentario, usuarioID, albumID):
    sql = 'INSERT INTO resenia (fecha, comentario, usuarioID, albumID) VALUES (%s,%s,%s,%s)'
    cursor.execute(sql, (datetime.today().strftime('%Y-%m-%d'), comentario, usuarioID, albumID))
    db.commit()

    return cursor.rowcount

def get_resenias():
    query = 'SELECT * FROM resenia'
    cursor.execute(query)

    resenias = []
    for row in cursor.fetchall():
        resenia = {
            "id": row[0],
            "fecha": row[1],
            "comentario": row[2],
            "usuarioID": row[3],
            "albumID": row[4]
        }
        resenias.append(resenia)
    
    return resenias
