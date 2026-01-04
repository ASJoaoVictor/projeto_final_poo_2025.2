from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.auth_controller import AuthController
from utils.exceptions import UsuarioJaExisteError, UsuarioInexistenteError

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


    try: 
        user = AuthController.login(email, password)
    except (UsuarioInexistenteError, UsuarioJaExisteError) as e:
        flash(str(e), "error")
        return redirect(url_for("auth_bp.login_page"))
    except Exception as e:
        flash("Ocorreu um erro inesperado. Tente novamente mais tarde.", "error")
        print("Erro de login:", e)
        return redirect(url_for("auth_bp.login_page"))
    
    return redirect(url_for("main_bp.dashboard_page"))
    
    

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("auth/register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AuthController.register(username, email, password)
    except UsuarioJaExisteError as e:
        flash(str(e), "error")
        return redirect(url_for("auth_bp.register_page"))
    except Exception as e:
        flash("Ocorreu um erro inesperado. Tente novamente mais tarde.", "error")
        print("Erro de registro:", e)
        return redirect(url_for("auth_bp.register_page"))

    flash("Usuário cadastrado com sucesso", "success")
    return redirect(url_for('auth_bp.login_page'))

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    AuthController.logout()
    return redirect(url_for("auth_bp.login_page"))