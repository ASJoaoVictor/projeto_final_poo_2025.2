from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.wallet_controller import WalletController
from controllers.transaction_controller import TransactionController
from controllers.category_controller import CategoryController
from flask_login import login_required, current_user

wallet_bp = Blueprint("wallet_bp", __name__, url_prefix="/wallet")

@wallet_bp.route("/new", methods=["GET"])
@login_required
def wallet_new_page():
    return render_template("wallet/new.html")

@wallet_bp.route("/create", methods=["POST"])
@login_required
def create_wallet():
    wallet_name = request.form.get("wallet_name").capitalize()
    initial_balance = request.form.get("initial_balance")

    wallet = WalletController.create_wallet(wallet_name, initial_balance, current_user.id)

    if wallet:
        flash("Nova carteira adicionado com sucesso!", "success")
        return redirect(url_for("main_bp.dashboard_page"))
    
    flash("Não foi possível adicionar nova carteira", "warning")
    return "deu problema"
    #return redirect(url_for("wallet_bp.wallet_new_page"))

@wallet_bp.route("/<int:wallet_id>", methods=["GET"])
@login_required
def wallet_detail_page(wallet_id):
    wallet = WalletController.get_wallet_by_id(wallet_id)
    transactions = TransactionController.get_transactions_by_wallet(wallet_id)
    #transactions = wallet.transactions
    categories = CategoryController.get_user_categories(user_id=current_user.id)

    if not wallet:
        return "Carteira não encontrada", 404
    
    if wallet.user_id != current_user.id:
        return "Acesso negado", 403
    
    return render_template("wallet/detail.html", wallet= wallet, transactions= transactions, categories= categories)

@wallet_bp.route("/<int:wallet_id>/delete", methods=["GET", "POST"])
def delete_wallet(wallet_id):
    #wallet = WalletController.deactivate_wallet(wallet_id, current_user.id)
    wallet = WalletController.delete_wallet(wallet_id, current_user.id)
    
    if not wallet:
        return "Carteira não encontrada ou acesso negado", 404
    
    flash("Carteira deletada com sucesso!", "success")
    return redirect(url_for("main_bp.dashboard_page"))

@wallet_bp.route("/<int:wallet_id>/edit", methods=["POST"])
@login_required
def edit_wallet(wallet_id):
    wallet_name = request.form.get("wallet_name").capitalize()
    #initial_balance = request.form.get("initial_balance")

    wallet = WalletController.edit_wallet(wallet_id, wallet_name, current_user.id)

    if wallet:
        flash("Carteira atualizada com sucesso!", "success")
        return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=wallet_id))
    
    flash("Não foi possível atualizar a carteira", "warning")
    return redirect(url_for("wallet_bp.wallet_detail_page", wallet_id=wallet_id))
