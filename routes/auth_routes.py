from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from controllers.auth_controller import AuthController
from flask_login import login_required, current_user

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
       return redirect(url_for("main_bp.dashboard_page"))
    return render_template("auth/login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    #pegar dados do form
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = AuthController.login(email, password)
    if user:
        return redirect(url_for("main_bp.dashboard_page"))
    
    flash("E-mail ou senha inválida", "error")
    return redirect(url_for("auth_bp.login_page"))
    

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("auth/register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user = AuthController.register(username, email, password)

    if user:
        flash("Usuário cadastrado com sucesso", "success")
        return redirect(url_for('auth_bp.login_page'))
    
    flash("E-mail já cadastro com outro usuário!", "warning")
    return redirect(url_for("auth_bp.register_page"))

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    AuthController.logout()
    return redirect(url_for("auth_bp.login_page"))