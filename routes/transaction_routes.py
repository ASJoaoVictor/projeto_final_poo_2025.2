from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController
from controllers.category_controller import CategoryController
from controllers.transaction_controller import TransactionController
from datetime import datetime


transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")

@transaction_bp.route("/", methods=["GET"])
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
    print("Creating transaction:", value, date, description, wallet_id, category_id, transaction_type)
    transaction = TransactionController.create_transaction(
        value=value,
        created_at=date,
        description=description,
        wallet_id=wallet_id,
        category_id=category_id,
        transaction_type=transaction_type,
        user_id=current_user.id
    )

    if transaction:
        flash("Transação criada com sucesso!", "success")
        return redirect(url_for("main_bp.dashboard_page"))

    flash("Não foi possível criar a transação", "warning")
    return redirect(url_for("transaction_bp.transaction_new_page"))


@transaction_bp.route("/edit")
@login_required
def transaction_edit():
    return "Em desenvolvimento"

@transaction_bp.route("/<int:transaction_id>/delete", methods=["POST"])
@login_required
def delete_transaction(transaction_id):
    transaction = TransactionController.delete_transaction(transaction_id, current_user.id)

    if not transaction:
        flash("Não foi possível deletar a transação", "warning")
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
    transaction = TransactionController.edit_transaction(
        transaction_id=transaction_id,
        value=value,
        created_at=date,
        description=description,
        category_id=category_id,
        user_id=current_user.id
    )

    if not transaction:
        flash("Não foi possível editar a transação", "warning")
        return redirect(request.referrer)
    
    flash("Transação editada com sucesso!", "success")
    #return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=transaction.wallet_id))
    return redirect(request.referrer)