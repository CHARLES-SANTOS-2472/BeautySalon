from app import create_app
from app.models.usuario import Usuario


app = create_app()

with app.app_context():
    usuarios = Usuario.query.all()

    for usuario in usuarios:
        print(
            f"ID: {usuario.id} | "
            f"Nome: {usuario.nome} | "
            f"E-mail: {usuario.email} | "
            f"Perfil: {usuario.perfil}"
        )