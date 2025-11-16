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

    def __str__(self):
        return f'Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Disponible: {self.disponible}'
