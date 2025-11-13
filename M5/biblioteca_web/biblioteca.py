import sqlite3

class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True
    
    def prestar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def devolver(self):
        if not self.disponible:
            self.disponible = True

    def __str__(self):
        return f'Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Disponible: {self.disponible}'

    def devolver(self):
        if self._prestado:
            self._prestado = False
            self.disponible = True

    def __str__(self):
        return f'Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Disponible: {self.disponible}'

class Biblioteca:
    libros = []
    
    def __init__(self, nombre):
        # Creamos la conexión a la base de datos
        self._conn = sqlite3.connect('biblioteca.db')
        self._conn.execute("PRAGMA foreign_keys = 1") # Habilitar claves foráneas para On DELETE CASCADE

        # Crear las tablas en la base de datos
        cursor = self._conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS biblioteca (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                isbn TEXT NOT NULL,
                disponible BOOLEAN NOT NULL,
                id_biblioteca INTEGER,
                FOREIGN KEY (id_biblioteca) REFERENCES biblioteca (id) ON DELETE CASCADE
            )
        ''')
        self._conn.commit()

        # Guardar la biblioteca en la base de datos
        cursor = self._conn.cursor()
        cursor.execute('''
            INSERT INTO biblioteca (nombre) VALUES (?)
        ''', (nombre,))
        self._conn.commit()

        self.nombre = nombre
        self._id = cursor.lastrowid

    def agregar_libro(self, libro):
        self.libros.append(libro)
        # Guardar el libro en la base de datos
        cursor = self._conn.cursor()
        cursor.execute('''
            INSERT INTO libro (titulo, autor, isbn, disponible, id_biblioteca)
            VALUES (?, ?, ?, ?, ?)
        ''', (libro.titulo, libro.autor, libro.isbn, libro.disponible, self._id))
        self._conn.commit()
        libro._id = cursor.lastrowid

    def mostrar_libros(self):
        for libro in self.libros:
            print(libro)

    def listar_libros(self):
        return self.libros
    
    def buscar_por_titulo(self, titulo):
        return [libro for libro in self.libros if libro.titulo == titulo]
    
    def prestar_libro(self, isbn):
        for libro in self.libros:
            if libro.isbn == isbn and libro.disponible:
                libro.prestar()
                # Actualizar en la base de datos
                cursor = self._conn.cursor()
                cursor.execute('''
                    UPDATE libro SET disponible = ? WHERE id = ?
                ''', (libro.disponible, libro._id))
                self._conn.commit()
                return True
        return False
    
    def borrar(self):
        # Eliminamos la tabla de la BD. Al tener ON DELETE CASCADE, se eliminan también los libros asociados.
        cursor = self._conn.cursor()
        cursor.execute('''
            DELETE FROM biblioteca WHERE id = ?
        ''', (self._id,))
        self._conn.commit()

    def borrar_libros(self):
        cursor = self._conn.cursor()
        cursor.execute('''
            DELETE FROM libro WHERE id_biblioteca = ?
        ''', (self._id,))
        self._conn.commit()
