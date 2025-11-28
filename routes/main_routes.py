from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/", methods=["GET"])
@login_required
def index_page():
    return render_template("index.html", user= current_user)