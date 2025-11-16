from biblioteca import Biblioteca, Libro
from flask import Flask, flash, redirect, render_template, request, url_for

# Inicializar la biblioteca
biblioteca = Biblioteca('Mi Biblioteca')
libros = []

app = Flask(__name__)
app.secret_key = 'Mi secreto'

# Rutas de la aplicación Flask
# Página principal con lista de libros y buscador
@app.route('/', methods=['GET', 'POST'])
def index():
    libros = biblioteca.cargar_libros()
    termino_busqueda = request.form.get('search', '').lower() if request.method == 'POST' else ''

    # Filtrar libros si hay término de búsqueda
    if termino_busqueda:
        libros = [
            libro for libro in libros
            if termino_busqueda in libro.titulo.lower() or
               termino_busqueda in libro.autor.lower() or
               termino_busqueda in libro.isbn.lower()
        ]

    return render_template('index.html', nombre=biblioteca.nombre, libros=libros, termino_busqueda=termino_busqueda)

# Página para agregar un libro
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        autor = request.form.get('autor', '').strip()
        isbn = request.form.get('isbn', '').strip()
        if not titulo or not autor or not isbn:
            flash('Todos los campos son obligatorios.', 'warning')
            return redirect(url_for('agregar'))
        libro = Libro(titulo, autor, isbn)
        try:
            biblioteca.agregar_libro(libro)
            flash('Libro agregado correctamente.', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('ISBN duplicado. No se pudo agregar el libro.', 'danger')
            return redirect(url_for('agregar'))
    return render_template('agregar.html')

# Ruta para prestar un libro
@app.route('/prestar/<isbn>')
def prestar(isbn):
    prestar = biblioteca.prestar_libro(isbn)
    if prestar:
        flash('El libro ha sido prestado.', 'success')
    else:
        flash('Libro no se puede prestar.', 'danger')
    return redirect(url_for('index'))

# Ruta para devolver un libro
@app.route('/devolver/<isbn>')
def devolver(isbn):
    devolver = biblioteca.devolver_libro(isbn)
    if devolver:
        flash('El libro ha sido devuelto.', 'success')
    else:
        flash('Libro no se puede devolver.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)