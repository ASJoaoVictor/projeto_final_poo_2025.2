from flask import Blueprint, render_template
from flask_login import login_required, current_user
from controllers.wallet_controller import WalletController

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    """Exibe a página principal (Dashboard) do usuário logado.

    Recupera as carteiras do usuário e calcula o saldo total consolidado
    somando o saldo atual de cada carteira.

    Returns:
        str: O template 'index.html' renderizado com as variáveis de contexto:
             - user: O objeto do usuário atual.
             - wallets: A lista de carteiras recuperadas.
             - total_balance: O somatório dos saldos das carteiras.
    """
    wallets = WalletController.get_wallets_by_user(current_user.id)

    total_balance = sum(wallet.current_balance for wallet in wallets)
    return render_template("index.html", user= current_user, wallets= wallets, total_balance=total_balance)