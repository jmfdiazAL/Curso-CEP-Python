# db_init.py
from models import db, DatabaseVersion
from app import create_app

app = create_app()
with app.app_context():
    db.create_all()
    # Establecer versión de la base de datos
    if not DatabaseVersion.query.first():
        db_version = DatabaseVersion(version='1.0')
        db.session.add(db_version)
        db.session.commit()
    print("Base de datos inicializada con versión 1.0")