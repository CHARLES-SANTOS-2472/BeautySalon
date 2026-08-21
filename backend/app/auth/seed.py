from app.models.usuario import Usuario
from app.extensions import db


def criar_admin():

    # Verifica se já existe algum usuário
    if Usuario.query.count() > 0:
        return

    admin = Usuario(
        nome="Administrador",
        email="admin@beautysalon.com",
        perfil="Administrador",
        ativo=True
    )

    admin.definir_senha("123456")

    db.session.add(admin)
    db.session.commit()

    print("✔ Usuário administrador criado com sucesso.")