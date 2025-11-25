from flask import Blueprint, render_template
from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth_dp", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def render_login():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    #pegar dados do form
    if AuthController.login():
        return "logado"

@auth_bp.route("/register", methods=["GET"])
def get_register():
    return render_template("register.html")