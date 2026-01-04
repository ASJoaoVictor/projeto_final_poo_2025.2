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
    transactions = TransactionController.get_user_transactions(user_id=current_user.id)
    total_income = sum(t.value for t in transactions if t.transaction_type == "income")
    total_expense = sum(t.value for t in transactions if t.transaction_type == "expense")
    total_balance = total_income - total_expense

    categories = CategoryController.get_user_categories(user_id= current_user.id)

    return render_template("transaction/index.html", 
                           transactions=transactions, 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           total_balance=total_balance,
                           categories = categories)

@transaction_bp.route("/new", methods=["GET"])
@login_required
def transaction_new_page():
    wallets = WalletController.get_wallets_by_user(user_id= current_user.id)
    categories = CategoryController.get_user_categories(user_id= current_user.id)

    return render_template("transaction/new.html", user_wallets= wallets, user_categories= categories)

@transaction_bp.route("/create", methods=["POST"])
@login_required
def transaction_create():
    value = request.form.get("value")
    date_str = request.form.get("date")
    description = request.form.get("description")
    wallet_id = request.form.get("wallet_id")
    category_id = request.form.get("category_id")
    transaction_type = request.form.get("transaction_type")

    date = datetime.strptime(date_str, "%Y-%m-%d")

    try:
        TransactionController.create_transaction(
            value=value,
            created_at=date,
            description=description,
            wallet_id=wallet_id,
            category_id=category_id,
            transaction_type=transaction_type,
            user_id=current_user.id
        )
    except CarteiraInexistenteError as e:
        flash(str(e), "warning")
        return redirect(url_for("transaction_bp.transaction_new_page"))
    except SaldoInsuficienteError as e:
        flash(str(e), "warning")
        return redirect(url_for("transaction_bp.transaction_new_page"))
    except CarteiraInexistenteError as e:
        flash(str(e), "warning")
        return redirect(url_for("transaction_bp.transaction_new_page"))
    except ValorInvalidoError as e:
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
    value = request.form.get("value")
    date_str = request.form.get("date")
    description = request.form.get("description").capitalize()
    category_id = request.form.get("category_id")

    date = datetime.strptime(date_str, "%Y-%m-%d")

    try:
        transaction = TransactionController.edit_transaction(
            transaction_id=transaction_id,
            value=value,
            created_at=date,
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