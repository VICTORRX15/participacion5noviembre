import sqlite3

def create_database():
    # Conexión a la base de datos
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()

    # Crear la tabla "producto"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Base de datos creada y tabla de productos inicializada.")
