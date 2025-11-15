from biblioteca import Biblioteca, Libro
from flask import Flask, render_template, request
import os

# Función para cargar libros
def cargar_libros(biblioteca):
    libros = []
    libros = biblioteca.listar_libros()
    return libros

# Inicializar la biblioteca
def init_biblioteca():
    biblioteca = Biblioteca('Mi Biblioteca')
    return biblioteca 

global biblioteca
biblioteca = init_biblioteca()

app = Flask(__name__)

# Rutas de la aplicación Flask
# Página principal con lista de libros y buscador
@app.route('/', methods=['GET', 'POST'])
def index():
    libros = cargar_libros(biblioteca)
    termino_busqueda = request.form.get('search', '').lower() if request.method == 'POST' else ''

    # Filtrar libros si hay término de búsqueda
    if termino_busqueda:
        libros = [
            libro for libro in libros
            if termino_busqueda in libro.titulo.lower() or
               termino_busqueda in libro.autor.lower() or
               termino_busqueda in libro.isbn.lower()
        ]

    return render_template('index.html', libros=libros, termino_busqueda=termino_busqueda)

# Página para agregar un libro
@app.route('/agregar', methods=["GET", "POST"])
def agregar():
    titulo = ""
    autor = ""
    isbn = ""
    if request.method == 'POST':
        titulo = request.form.get("titulo")
        autor = request.form.get("autor")
        isbn = request.form.get("isbn")
        biblioteca.agregar_libro(Libro(titulo, autor, isbn))  

    return render_template("agregar.html", titulo=titulo, autor=autor, isbn=isbn)

@app.route('/prestar/<isbn>', methods=['GET', 'POST'])
def prestar(isbn):
    libros = cargar_libros(biblioteca)
    return render_template('index.html', libros=libros, mensaje=isbn)

if __name__ == '__main__':
    app.run(debug=True)