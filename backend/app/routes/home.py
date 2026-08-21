from flask import Blueprint

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():

    return {
        "status":"online",
        "sistema":"Beauty Salon",
        "versao":"1.0"
    }