from flask import Blueprint, render_template, request, flash
from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth_dp", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def render_login():
    flash("teste", "alert-info")
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    #pegar dados do form
    username = request.form.get("username")
    password = request.form.get("password")

    if AuthController.login(username, password):
        return "Logado"
    
    return render_login()
    

@auth_bp.route("/register", methods=["GET"])
def render_register():
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)
    user = AuthController.register(email, password)

    if user:
        return "Cadastrado com sucesso"
    
    return "deu errado"

@auth_bp.route("/logoff", methods=["GET", "POST"])
def logoff():
    return "logoff..."