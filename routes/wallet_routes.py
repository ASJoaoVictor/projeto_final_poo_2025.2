from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController
from controllers.transaction_controller import TransactionController
from controllers.category_controller import CategoryController
from utils.exceptions import ValorInvalidoError, CarteiraJaExisteError, CategoriaInvalidaError, CarteiraInexistenteError, AcessoNegadoError

wallet_bp = Blueprint("wallet_bp", __name__, url_prefix="/wallet")

@wallet_bp.route("/new", methods=["GET"])
@login_required
def wallet_new_page():
    """Exibe o formulário de criação de uma nova carteira.

    Returns:
        str: O template 'wallet/new.html'.
    """
    return render_template("wallet/new.html")

@wallet_bp.route("/create", methods=["POST"])
@login_required
def create_wallet():
    """Processa a criação de uma nova carteira.

    Recebe o nome e o saldo inicial do formulário. Tenta criar a carteira
    através do WalletController.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para o dashboard em caso de sucesso
        ou recarga da página de criação em caso de erro.
    """
    wallet_name = request.form.get("wallet_name").capitalize()
    initial_balance = request.form.get("initial_balance")

    try:
        WalletController.create_wallet(wallet_name, initial_balance, current_user.id)
    except (ValorInvalidoError, CarteiraJaExisteError, CategoriaInvalidaError) as e:
        flash(str(e), "warning")
        return redirect(url_for("wallet_bp.wallet_new_page"))
    except Exception as e:
        flash("Não foi possível criar a carteira. Tente novamente mais tarde.", "error")
        print(f"Erro não tratado: {e}")
        return redirect(url_for("wallet_bp.wallet_new_page"))

    flash("Nova carteira adicionado com sucesso!", "success")
    return redirect(url_for("main_bp.dashboard_page"))    

@wallet_bp.route("/<int:wallet_id>", methods=["GET"])
@login_required
def wallet_detail_page(wallet_id):
    """Exibe os detalhes de uma carteira específica.

    Mostra o saldo atual e o histórico de transações vinculadas a esta carteira.
    Verifica se a carteira pertence ao usuário logado.

    Args:
        wallet_id (int): O ID da carteira a ser visualizada.

    Returns:
        str: O template 'wallet/detail.html' com dados da carteira, transações e categorias.
    """
    try:
        wallet = WalletController.get_wallet_by_id(wallet_id, current_user.id)
    except CarteiraInexistenteError as e:
        flash(str(e), "error")
        return redirect(url_for("main_bp.dashboard_page"))  
    
    transactions = TransactionController.get_transactions_by_wallet(wallet_id)
    categories = CategoryController.get_user_categories(user_id=current_user.id)

    return render_template("wallet/detail.html", wallet= wallet, transactions= transactions, categories= categories)

@wallet_bp.route("/<int:wallet_id>/delete", methods=["POST"])
@login_required
def delete_wallet(wallet_id):
    """Remove uma carteira do sistema.

    Exclui a carteira permanentemente (ou logicamente, dependendo da implementação do Controller).

    Args:
        wallet_id (int): O ID da carteira a ser removida.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para o dashboard.
    """
    try:
        WalletController.delete_wallet(wallet_id, current_user.id)
        #wallet = WalletController.deactivate_wallet(wallet_id, current_user.id)
    except AcessoNegadoError as e:
        flash(str(e), "error")
        return redirect(url_for("main_bp.dashboard_page"))
    except CarteiraInexistenteError as e:
        flash(str(e), "error")
        return redirect(url_for("main_bp.dashboard_page"))
    except Exception as e:
        flash("Não foi possível deletar a carteira. Tente novamente mais tarde.", "error")
        print(f"Erro não tratado: {e}")
        return redirect(url_for("main_bp.dashboard_page"))

    flash("Carteira deletada com sucesso!", "success")
    return redirect(url_for("main_bp.dashboard_page"))

@wallet_bp.route("/<int:wallet_id>/edit", methods=["POST"])
@login_required
def edit_wallet(wallet_id):
    """Edita as informações básicas de uma carteira (ex: nome).

    Args:
        wallet_id (int): O ID da carteira a ser editada.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento de volta para a página de detalhes da carteira.
    """
    wallet_name = request.form.get("wallet_name").capitalize()

    try:
        WalletController.edit_wallet(wallet_id, wallet_name, current_user.id)
    except CarteiraInexistenteError as e:
        flash(str(e), "error")
        return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=wallet_id))
    except CarteiraJaExisteError as e:
        flash(str(e), "warning")
        return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=wallet_id))
    except Exception as e:
        flash("Não foi possível editar a carteira. Tente novamente mais tarde.", "error")
        print(f"Erro não tratado: {e}")
        return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=wallet_id))

    flash("Carteira atualizada com sucesso!", "success")
    return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=wallet_id))

