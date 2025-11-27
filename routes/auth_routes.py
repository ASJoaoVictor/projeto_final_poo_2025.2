from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from controllers.auth_controller import AuthController
from flask_login import login_required, current_user

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
       return render_template("dashboard.html")
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    #pegar dados do form
    email = request.form.get("email")
    password = request.form.get("password")

    if AuthController.login(email, password):
        return render_template("dashboard.html")
    
    return render_login()
    

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    user = AuthController.register(email, password)

    if user:
        flash("Usuário cadastrado")
        return redirect(url_for('auth_bp.render_login'))
    
    return "deu errado"

@auth_bp.route("/logoff", methods=["GET", "POST"])
@login_required
def logout():
    AuthController.logout()
    return redirect(url_for("auth_bp.login_page"))