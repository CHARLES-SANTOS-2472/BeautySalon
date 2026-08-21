from app.extensions import db

class CategoriaServico(db.Model):

    __tablename__ = "categorias_servico"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(80), nullable=False)