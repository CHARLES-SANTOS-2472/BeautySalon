from app import create_app
from app.extensions import db
from app.models.usuario import Usuario


NOVO_EMAIL = "editcha.editcha@gmail.com"

app = create_app()

with app.app_context():
    administrador = Usuario.query.get(1)

    if administrador is None:
        print("Administrador não encontrado.")
    else:
        administrador.email = NOVO_EMAIL
        db.session.commit()

        print(
            "E-mail atualizado para: "
            f"{administrador.email}"
        )