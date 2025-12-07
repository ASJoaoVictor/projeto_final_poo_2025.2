from flask import Blueprint, render_template


transaction_bp = Blueprint("transaction_bp", __name__, url_prefix="/transaction")

@transaction_bp.route("/new", methods=["GET"])
def wallet_new_page():
    return render_template("transaction/new.html")

@transaction_bp.route("/create", methods=["POST"])
def transaction_create():
    return "ainda não está funcionando"