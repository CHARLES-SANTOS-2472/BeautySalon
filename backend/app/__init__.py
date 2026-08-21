from flask import Flask
from sqlalchemy.exc import OperationalError

from .config import Config
from .extensions import db, migrate, jwt

from .routes.home import home_bp
from .routes.usuarios import usuarios_bp
from .routes.auth import auth_bp
from .routes.clientes import clientes_bp
from .routes.agendamentos import agendamentos_bp
from .routes.funcionarios import funcionarios_bp
from .routes.categorias_servico import categorias_servico_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(agendamentos_bp)
    app.register_blueprint(funcionarios_bp)
    app.register_blueprint(categorias_servico_bp)

    with app.app_context():

        try:
            from app.auth.seed import criar_admin

            criar_admin()
            
        except Exception:

            pass


    return app









"""from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .routes.home import home_bp
from .routes.usuarios import usuarios_bp
from .routes.auth import auth_bp
from .routes.clientes import clientes_bp
from .routes.agendamentos import agendamentos_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(agendamentos_bp)

    with app.app_context():

        try:
            from app.auth.seed import criar_admin

            criar_admin()
            
        except OperationalError:
                
            print("Banco de dados ainda não foi criado.")
            

    return app"""