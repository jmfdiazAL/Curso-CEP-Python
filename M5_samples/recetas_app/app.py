from flask import Flask, render_template, request
import os
import markdown
import frontmatter

app = Flask(__name__)
RECETAS_DIR = 'recetas'

# Función para cargar y procesar recetas
def cargar_recetas():
    recetas = []
    for archivo in os.listdir(RECETAS_DIR):
        if archivo.endswith('.md'):
            with open(os.path.join(RECETAS_DIR, archivo), 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                recetas.append({
                    'filename': archivo,
                    'title': post.get('title', archivo.replace('.md', '')),
                    'content': post.content,
                    'category': post.get('category', ''),
                    'tags': post.get('tags', [])
                })
    return recetas

# Página principal con lista de recetas y buscador
@app.route('/', methods=['GET', 'POST'])
def index():
    recetas = cargar_recetas()
    termino_busqueda = request.form.get('search', '').lower() if request.method == 'POST' else ''

    # Filtrar recetas si hay término de búsqueda
    if termino_busqueda:
        recetas = [
            receta for receta in recetas
            if termino_busqueda in receta['title'].lower() or
               termino_busqueda in receta['content'].lower() or
               any(termino_busqueda in tag.lower() for tag in receta['tags'])
        ]

    return render_template('index.html', recetas=recetas, termino_busqueda=termino_busqueda)

# Página individual de receta
@app.route('/receta/<nombre>')
def receta(nombre):
    try:
        with open(os.path.join(RECETAS_DIR, nombre), 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            html = markdown.markdown(post.content, extensions=['extra'])
            return render_template('receta.html', html=html, title=post.get('title', nombre))
    except FileNotFoundError:
        return "Receta no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)