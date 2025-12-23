from flask import Blueprint, render_template
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    wallets = WalletController.get_wallets_by_user(current_user.id)

    total_balance = sum(wallet.current_balance for wallet in wallets)
    print(total_balance)
    return render_template("index.html", user= current_user, wallets= wallets, total_balance=total_balance)