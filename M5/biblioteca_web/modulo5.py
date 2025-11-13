from biblioteca import Biblioteca, Libro

biblioteca = Biblioteca('Biblioteca Central')

biblioteca.agregar_libro(Libro('Cien Años de Soledad', 'Gabriel García Márquez', '978-3-16-148410-0'))
biblioteca.agregar_libro(Libro('Don Quijote de la Mancha', 'Miguel de Cervantes', '978-1-56619-909-4'))
biblioteca.agregar_libro(Libro('La Sombra del Viento', 'Carlos Ruiz Zafón', '978-0-7432-7356-5'))
biblioteca.agregar_libro(Libro('El Amor en los Tiempos del Cólera', 'Gabriel García Márquez', '978-0-307-38912-9'))
biblioteca.agregar_libro(Libro('La Ciudad y los Perros', 'Mario Vargas Llosa', '978-0-14-303995-2'))
biblioteca.agregar_libro(Libro('Ficciones', 'Jorge Luis Borges', '978-0-14-118280-3'))

biblioteca.mostrar_libros()
biblioteca.prestar_libro('978-1-56619-909-4')
# ISBN no existente
if not biblioteca.prestar_libro('ISBN-INVALIDO'):
    print("El libro no se puede prestar.")
    if not isinstance('ISBN-INVALIDO', str) == 0:
        print("El libro no se encuentra en la biblioteca.")

biblioteca.mostrar_libros()

biblioteca.borrar()
