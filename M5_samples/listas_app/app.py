# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Usuario, Lista, Item, Etiqueta, ListaEtiqueta, ItemEtiqueta, Favorito, Suscripcion, Like, Checked, DatabaseVersion
import bcrypt
import csv
import io
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listas_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    return app

app = create_app()

# Rutas
@app.route('/')
def index():
    listas = Lista.query.filter_by(visibilidad='publica').all()
    return render_template('listas.html', listas=listas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.checkpw(contrasena.encode('utf-8'), usuario.contrasena.encode('utf-8')):
            login_user(usuario)
            return redirect(url_for('index'))
        flash('Credenciales inválidas')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        email = request.form['email']
        contrasena = bcrypt.hashpw(request.form['contrasena'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario = Usuario(nombre_usuario=nombre_usuario, email=email, contrasena=contrasena)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario registrado')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/lista/crear', methods=['GET', 'POST'])
@login_required
def crear_lista():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        imagen = request.form.get('imagen')
        visibilidad = request.form['visibilidad']
        lista = Lista(id_usuario=current_user.id, titulo=titulo, descripcion=descripcion, imagen=imagen, visibilidad=visibilidad)
        db.session.add(lista)
        db.session.commit()
        etiquetas = request.form.get('etiquetas', '').split(',')
        for etiqueta in etiquetas:
            etiqueta = etiqueta.strip()
            if etiqueta:
                tag = Etiqueta.query.filter_by(nombre=etiqueta).first() or Etiqueta(nombre=etiqueta)
                db.session.add(tag)
                db.session.commit()
                lista_etiqueta = ListaEtiqueta(id_lista=lista.id, id_etiqueta=tag.id)
                db.session.add(lista_etiqueta)
        db.session.commit()
        return redirect(url_for('ver_lista', id_lista=lista.id))
    return render_template('lista.html', lista=None)

@app.route('/lista/<int:id_lista>', methods=['GET', 'POST'])
def ver_lista(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if lista.visibilidad == 'privada' and (not current_user.is_authenticated or current_user.id != lista.id_usuario):
        flash('No tienes acceso a esta lista')
        return redirect(url_for('index'))
    filtro_etiquetas = request.args.get('etiquetas', '').split(',') if request.args.get('etiquetas') else []
    items = Item.query.filter_by(id_lista=id_lista).order_by(Item.orden).all()
    if filtro_etiquetas:
        items = [item for item in items if any(ie.id_etiqueta in [Etiqueta.query.filter_by(nombre=tag).first().id for tag in filtro_etiquetas if Etiqueta.query.filter_by(nombre=tag).first()] for ie in ItemEtiqueta.query.filter_by(id_item=item.id).all())]
    return render_template('lista.html', lista=lista, items=items, filtro_etiquetas=filtro_etiquetas)

@app.route('/lista/<int:id_lista>/item', methods=['POST'])
@login_required
def agregar_item(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if lista.id_usuario != current_user.id:
        flash('No tienes permiso para modificar esta lista')
        return redirect(url_for('ver_lista', id_lista=id_lista))
    descripcion = request.form['descripcion']
    enlace = request.form.get('enlace')
    imagen = request.form.get('imagen')
    orden = request.form.get('orden', type=int, default=Item.query.filter_by(id_lista=id_lista).count())
    item = Item(id_lista=id_lista, descripcion=descripcion, enlace=enlace, imagen=imagen, orden=orden)
    db.session.add(item)
    db.session.commit()
    etiquetas = request.form.get('etiquetas', '').split(',')
    for etiqueta in etiquetas:
        etiqueta = etiqueta.strip()
        if etiqueta:
            tag = Etiqueta.query.filter_by(nombre=etiqueta).first() or Etiqueta(nombre=etiqueta)
            db.session.add(tag)
            db.session.commit()
            item_etiqueta = ItemEtiqueta(id_item=item.id, id_etiqueta=tag.id)
            db.session.add(item_etiqueta)
    db.session.commit()
    return redirect(url_for('ver_lista', id_lista=id_lista))

@app.route('/lista/<int:id_lista>/duplicar', methods=['POST'])
@login_required
def duplicar_lista(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if lista.visibilidad == 'privada' and lista.id_usuario != current_user.id:
        flash('No tienes acceso a esta lista')
        return redirect(url_for('index'))
    nueva_lista = Lista(
        id_usuario=current_user.id,
        titulo=f"{lista.titulo} (Copia)",
        descripcion=lista.descripcion,
        imagen=lista.imagen,
        visibilidad='privada',
        fecha_creacion=datetime.utcnow()
    )
    db.session.add(nueva_lista)
    db.session.commit()
    for item in lista.items:
        nuevo_item = Item(
            id_lista=nueva_lista.id,
            descripcion=item.descripcion,
            enlace=item.enlace,
            imagen=item.imagen,
            orden=item.orden
        )
        db.session.add(nuevo_item)
        db.session.commit()
        for item_etiqueta in ItemEtiqueta.query.filter_by(id_item=item.id).all():
            nueva_item_etiqueta = ItemEtiqueta(id_item=nuevo_item.id, id_etiqueta=item_etiqueta.id_etiqueta)
            db.session.add(nueva_item_etiqueta)
    for lista_etiqueta in ListaEtiqueta.query.filter_by(id_lista=lista.id).all():
        nueva_lista_etiqueta = ListaEtiqueta(id_lista=nueva_lista.id, id_etiqueta=lista_etiqueta.id_etiqueta)
        db.session.add(nueva_lista_etiqueta)
    db.session.commit()
    return redirect(url_for('ver_lista', id_lista=nueva_lista.id))

@app.route('/lista/<int:id_lista>/like', methods=['POST'])
@login_required
def like_lista(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if Like.query.filter_by(id_usuario=current_user.id, id_lista=id_lista).first():
        flash('Ya diste like a esta lista')
    else:
        like = Like(id_usuario=current_user.id, id_lista=id_lista)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('ver_lista', id_lista=id_lista))

@app.route('/item/<int:id_item>/like', methods=['POST'])
@login_required
def like_item(id_item):
    item = Item.query.get_or_404(id_item)
    if Like.query.filter_by(id_usuario=current_user.id, id_item=id_item).first():
        flash('Ya diste like a este item')
    else:
        like = Like(id_usuario=current_user.id, id_item=id_item)
        db.session.add(like)
        db.session.commit()
    return redirect(url_for('ver_lista', id_lista=item.id_lista))

@app.route('/item/<int:id_item>/check', methods=['POST'])
@login_required
def check_item(id_item):
    item = Item.query.get_or_404(id_item)
    if Checked.query.filter_by(id_usuario=current_user.id, id_item=id_item).first():
        flash('Item ya marcado como checked')
    else:
        checked = Checked(id_usuario=current_user.id, id_item=id_item)
        db.session.add(checked)
        db.session.commit()
    return redirect(url_for('ver_lista', id_lista=item.id_lista))

@app.route('/lista/<int:id_lista>/favorito', methods=['POST'])
@login_required
def favorito_lista(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if Favorito.query.filter_by(id_usuario=current_user.id, id_lista=id_lista).first():
        flash('Lista ya en favoritos')
    else:
        favorito = Favorito(id_usuario=current_user.id, id_lista=id_lista)
        lista.contador_favoritos += 1
        db.session.add(favorito)
        db.session.commit()
    return redirect(url_for('ver_lista', id_lista=id_lista))

@app.route('/lista/<int:id_lista>/suscribir', methods=['POST'])
@login_required
def suscribir_lista(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if Suscripcion.query.filter_by(id_usuario=current_user.id, id_lista=id_lista).first():
        flash('Ya estás suscrito a esta lista')
    else:
        suscripcion = Suscripcion(id_usuario=current_user.id, id_lista=id_lista)
        db.session.add(suscripcion)
        db.session.commit()
    return redirect(url_for('ver_lista', id_lista=id_lista))

@app.route('/lista/<int:id_lista>/exportar/csv')
def exportar_csv(id_lista):
    lista = Lista.query.get_or_404(id_lista)
    if lista.visibilidad == 'privada' and (not current_user.is_authenticated or current_user.id != lista.id_usuario):
        flash('No tienes acceso a esta lista')
        return redirect(url_for('index'))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['titulo_lista', 'descripcion_lista', 'imagen_lista', 'etiquetas_lista', 'id_item', 'descripcion_item', 'enlace_item', 'imagen_item', 'etiquetas_item', 'orden_item'])
    etiquetas_lista = ','.join([le.etiqueta.nombre for le in ListaEtiqueta.query.filter_by(id_lista=lista.id).all()])
    for item in lista.items:
        etiquetas_item = ','.join([ie.etiqueta.nombre for ie in ItemEtiqueta.query.filter_by(id_item=item.id).all()])
        writer.writerow([lista.titulo, lista.descripcion, lista.imagen, etiquetas_lista, item.id, item.descripcion, item.enlace, item.imagen, etiquetas_item, item.orden])
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name=f'lista_{id_lista}.csv')

if __name__ == '__main__':
    app.run(debug=True)