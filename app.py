from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'mi_secreto'

DATABASE = 'almacen.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Ruta para ver todos los productos
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        # Validación de datos
        if not descripcion or not cantidad or not precio:
            flash('Todos los campos son requeridos.')
            return redirect(url_for('agregar'))

        conn = get_db_connection()
        conn.execute('INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)',
                     (descripcion, cantidad, precio))
        conn.commit()
        conn.close()
        flash('Producto agregado exitosamente.')
        return redirect(url_for('index'))

    return render_template('agregar.html')

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        # Validación de datos
        if not descripcion or not cantidad or not precio:
            flash('Todos los campos son requeridos.')
            return redirect(url_for('editar', id=id))

        conn = get_db_connection()
        conn.execute('UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?',
                     (descripcion, cantidad, precio, id))
        conn.commit()
        conn.close()
        flash('Producto actualizado exitosamente.')
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
