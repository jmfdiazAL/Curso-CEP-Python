from biblioteca import Biblioteca, Libro
from flask import Flask, request

app = Flask('Biblioteca')

@app.route('/')
def index():
    return 'Biblioteca'
@app.route('/test')
def test():
    return 'test Flask'


@app.route('/prestar',methods = ["GET", "POST"])
@app.route('/suma/',methods = ["GET", "POST"])
def suma():
    htmlCode = ""
    if request.method == "POST":
        print("POST") # Obtenemos datos y calcula
        sumando1 = int(request.form.get("Sumando1"))
        sumando2 = int(request.form.get("Sumando2"))
        htmlCode = "Resultado: " +  str(sumando1 +sumando2)
    else:
        print("GET") # Mostramos HTML
        htmlCode = '''<form action="/suma" method="POST">
                <label>Sumando 1:</label>
                <input type="text" name="Sumando1"/>
                <label>Sumando 2:</label>
                <input type="text" name="Sumando2"/><br/><br/>
                <input type="submit"/>
                </form>'''
    return htmlCode

biblioteca = Biblioteca('Biblioteca Central')

biblioteca.agregar_libro(Libro('Cien Años de Soledad', 'Gabriel García Márquez', '978-3-16-148410-0'))
biblioteca.agregar_libro(Libro('Don Quijote de la Mancha', 'Miguel de Cervantes', '978-1-56619-909-4'))
biblioteca.agregar_libro(Libro('La Sombra del Viento', 'Carlos Ruiz Zafón', '978-0-7432-7356-5'))

if __name__ == '__main__':
    app.run(debug = False, host='127.0.0.1') # solo acceso local y puerto 5000
