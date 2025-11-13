from biblioteca import Biblioteca, Libro
from flask import Flask, render_template, request
import os
import markdown
import frontmatter

# Función para cargar libros
def cargar_libros(biblioteca):
    libros = []
    libros = biblioteca.listar_libros()
    return libros

app = Flask(__name__)

# Inicializar la biblioteca
biblioteca = Biblioteca("Mi Biblioteca")
# Borrar libros existentes para evitar duplicados en cada ejecución
biblioteca.borrar_libros()
# Agregar libros de ejemplo
biblioteca.agregar_libro(Libro('Cien Años de Soledad', 'Gabriel García Márquez', '978-3-16-148410-0'))
biblioteca.agregar_libro(Libro('Don Quijote de la Mancha', 'Miguel de Cervantes', '978-1-56619-909-4'))
biblioteca.agregar_libro(Libro('La Sombra del Viento', 'Carlos Ruiz Zafón', '978-0-7432-7356-5'))
biblioteca.agregar_libro(Libro('El Amor en los Tiempos del Cólera', 'Gabriel García Márquez', '978-0-307-38912-9'))
biblioteca.agregar_libro(Libro('La Ciudad y los Perros', 'Mario Vargas Llosa', '978-0-14-303995-2'))
biblioteca.agregar_libro(Libro('Ficciones', 'Jorge Luis Borges', '978-0-14-118280-3'))  

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

if __name__ == '__main__':
    app.run(debug=True)