from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController
from controllers.category_controller import CategoryController
from controllers.transaction_controller import TransactionController
from utils.exceptions import CarteiraInexistenteError, SaldoInsuficienteError, CarteiraInexistenteError, ValorInvalidoError, TransacaoInexistenteError
from datetime import datetime


transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")

@transaction_bp.route("", methods=["GET"])
@login_required
def transaction_page():
    """Exibe o histórico de transações filtrado por mês e ano.

    Calcula os totais (Receitas, Despesas e Saldo) com base nas transações
    do período selecionado. Se nenhum mês/ano for informado, utiliza a data atual.

    Query Args:
        month (int, optional): Mês para filtro (padrão: mês atual).
        year (int, optional): Ano para filtro (padrão: ano atual).

    Returns:
        str: O template 'transaction/index.html' com a lista de transações e o sumário financeiro.
    """
    today = datetime.now()

    selected_month = request.args.get("month", today.month, type=int)
    selected_year = request.args.get("year", today.year, type=int)

    transactions = TransactionController.get_user_transactions(
        user_id=current_user.id,
        month=selected_month,
        year=selected_year
    )
    
    total_income = sum(t.value for t in transactions if t.transaction_type == "income")
    total_expense = sum(t.value for t in transactions if t.transaction_type == "expense")
    total_balance = total_income - total_expense

    categories = CategoryController.get_user_categories(user_id= current_user.id)

    return render_template("transaction/index.html", 
                           transactions=transactions, 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           total_balance=total_balance,
                           categories = categories,
                           selected_month=selected_month,
                           selected_year=selected_year)

@transaction_bp.route("/new", methods=["GET"])
@login_required
def transaction_new_page():
    """Exibe o formulário para criação de uma nova transação.

    Carrega as carteiras e categorias do usuário para preencher os campos de seleção (dropdowns).

    Returns:
        str: O template 'transaction/new.html'.
    """
    wallets = WalletController.get_wallets_by_user(user_id= current_user.id)
    categories = CategoryController.get_user_categories(user_id= current_user.id)

    return render_template("transaction/new.html", user_wallets= wallets, user_categories= categories)

@transaction_bp.route("/create", methods=["POST"])
@login_required
def transaction_create():
    """Processa a criação de uma nova transação.

    Coleta os dados do formulário e delega a validação e conversão de tipos
    (incluindo a data) para o TransactionController.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para o dashboard em sucesso
        ou recarga do formulário em caso de falha.
    """
    value = request.form.get("value")
    date_str = request.form.get("date")
    description = request.form.get("description")
    wallet_id = request.form.get("wallet_id")
    category_id = request.form.get("category_id")
    transaction_type = request.form.get("transaction_type")

    try:
        TransactionController.create_transaction(
            value=value,
            date_str=date_str,
            description=description,
            wallet_id=wallet_id,
            category_id=category_id,
            transaction_type=transaction_type,
            user_id=current_user.id
        )
    except (CarteiraInexistenteError, SaldoInsuficienteError, ValorInvalidoError) as e:
        flash(str(e), "warning")
        return redirect(url_for("transaction_bp.transaction_new_page"))
    except Exception as e:
        flash("Ocorreu um erro ao criar a transação.", "error")
        print("Erro não tratado:", e)
        return redirect(url_for("transaction_bp.transaction_new_page"))
    

    flash("Transação criada com sucesso!", "success")
    return redirect(url_for("main_bp.dashboard_page"))

@transaction_bp.route("/<int:transaction_id>/delete", methods=["POST"])
@login_required
def delete_transaction(transaction_id):
    """Remove uma transação.

    Tenta excluir a transação e retorna o usuário para a página de origem.

    Args:
        transaction_id (int): ID da transação a ser excluída.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para a página anterior (referrer)
        ou para o dashboard caso o referrer não exista.
    """
    try:
        TransactionController.delete_transaction(transaction_id, current_user.id)
    except CarteiraInexistenteError as e:
        flash(str(e), "warning")
        return redirect(request.referrer)
    except TransacaoInexistenteError as e:
        flash(str(e), "warning")
        return redirect(request.referrer)
    except Exception as e:
        flash("Ocorreu um erro ao deletar a transação.", "error")
        print("Erro não tratado:", e)
        return redirect(request.referrer)
    
    flash("Transação deletada com sucesso!", "success")
    return redirect(request.referrer)

@transaction_bp.route("/<int:transaction_id>/edit", methods=["POST"])
@login_required
def edit_transaction(transaction_id):
    """Edita uma transação existente.

    Passa os dados brutos (incluindo a data como string) para o Controller validar.

    Args:
        transaction_id (int): ID da transação a ser editada.

    Returns:
        Werkzeug.wrappers.response.Response: Redirecionamento para a página anterior.
    """
    value = request.form.get("value")
    date_str = request.form.get("date")
    description = request.form.get("description").capitalize()
    category_id = request.form.get("category_id")

    try:
        transaction = TransactionController.edit_transaction(
            transaction_id=transaction_id,
            value=value,
            date_str=date_str,
            description=description,
            category_id=category_id,
            user_id=current_user.id
        )
    except CarteiraInexistenteError as e:
        flash(str(e), "warning")
        return redirect(request.referrer)
    except ValorInvalidoError as e:
        flash(str(e), "warning")
        return redirect(request.referrer)
    except TransacaoInexistenteError as e:
        flash(str(e), "warning")
        return redirect(request.referrer)
    except Exception as e:
        flash("Ocorreu um erro ao editar a transação.", "error")
        print("Erro não tratado:", e)
        return redirect(request.referrer)

    flash("Transação editada com sucesso!", "success")
    return redirect(request.referrer)