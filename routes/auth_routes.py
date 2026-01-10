from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.auth_controller import AuthController
from utils.exceptions import UsuarioJaExisteError, UsuarioInexistenteError, SenhasDiferentes

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    """Exibe a página de login.

    Verifica se o usuário já está autenticado. Se sim, redireciona diretamente
    para o dashboard, evitando logins redundantes. Caso contrário, renderiza
    o formulário de acesso.

    Returns:
        str|Werkzeug.wrappers.response.Response: O template HTML de login ou um 
        redirecionamento para o dashboard.
    """
    if current_user.is_authenticated:
       return redirect(url_for("main_bp.dashboard_page"))
    return render_template("auth/login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    """Processa a submissão do formulário de login.

    Captura email e senha do formulário e tenta autenticar via AuthController.
    Em caso de sucesso, redireciona para o dashboard. Em caso de falha (usuário
    não encontrado ou dados incorretos), exibe uma mensagem flash e recarrega a página.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para dashboard (sucesso) 
        ou login (erro).
    """
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
    """Exibe a página de cadastro de novos usuários.

    Returns:
        str: O template HTML de registro.
    """
    return render_template("auth/register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    """Processa a criação de uma nova conta de usuário.

    Recebe username, email e senha. Se o cadastro for bem-sucedido, exibe uma
    mensagem de sucesso e redireciona para o login. Se houver conflito (email já existe)
    ou erro, exibe mensagem de erro e mantém na página de registro.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para login (sucesso) 
        ou recarga da página de registro (erro).
    """
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    try:
        user = AuthController.register(username, email, password, confirm_password)
    except (UsuarioInexistenteError, SenhasDiferentes) as e:
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
    """Encerra a sessão do usuário atual.

    Chama o controller para limpar a sessão de autenticação e redireciona
    o usuário para a tela de login. Requer que o usuário esteja logado.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para a página de login.
    """
    AuthController.logout()
    return redirect(url_for("auth_bp.login_page"))