from flask import Blueprint, render_template
from flask_login import login_required, current_user
from controllers.category_controller import CategoryController

category_bp = Blueprint("category_bp", __name__, url_prefix="/category")

@category_bp.route("/new", methods=["GET"])
@login_required
def category_new_page():
    user_categories = CategoryController.get_user_categories(current_user.id)

    return render_template("category/new.html")