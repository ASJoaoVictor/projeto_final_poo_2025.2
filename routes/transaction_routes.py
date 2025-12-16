from flask import Blueprint, render_template
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController
from controllers.category_controller import CategoryController


transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")

@transaction_bp.route("/new", methods=["GET"])
def transaction_new_page():
    wallets = WalletController.get_wallets_by_user(user_id= current_user.id)
    categories = CategoryController.get_user_categories(user_id= current_user.id)

    return render_template("transaction/new.html", user_wallets= wallets)

@transaction_bp.route("/create", methods=["POST"])
def transaction_create():
    return "ainda não está funcionando"

@transaction_bp.route("/edit")
def transaction_edit():
    return "Em desenvolvimento"