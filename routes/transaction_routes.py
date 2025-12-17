from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController
from controllers.category_controller import CategoryController
from controllers.transaction_controller import TransactionController


transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")

@transaction_bp.route("/new", methods=["GET"])
def transaction_new_page():
    wallets = WalletController.get_wallets_by_user(user_id= current_user.id)
    categories = CategoryController.get_user_categories(user_id= current_user.id)

    return render_template("transaction/new.html", user_wallets= wallets, user_categories= categories)

@transaction_bp.route("/create", methods=["POST"])
def transaction_create():
    value = request.form.get("value")
    date = request.form.get("date")
    description = request.form.get("description")
    wallet_id = request.form.get("wallet_id")
    category_id = request.form.get("category_id")
    transaction_type = request.form.get("transaction_type")

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
    return redirect(url_for("main_bp.dashboard_page"))
    return redirect(url_for("transaction_bp.transaction_new_page"))


@transaction_bp.route("/edit")
def transaction_edit():
    return "Em desenvolvimento"