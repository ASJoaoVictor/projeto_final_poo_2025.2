from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from controllers.category_controller import CategoryController

category_bp = Blueprint("category_bp", __name__, url_prefix="/category")

@category_bp.route("/index", methods=["GET"])
@login_required
def category_index_page():
    user_categories = CategoryController.get_user_categories(current_user.id)

    return render_template("category/index.html", categories= user_categories)

@category_bp.route("/create", methods=["POST"])
@login_required
def create_category():
    category_name = request.form.get("category_name").capitalize()

    category = CategoryController.create_category(category_name, current_user.id)

    if category:
        flash("Nova categoria adicionada com sucesso!", "success")
        return redirect(url_for("category_bp.category_index_page"))
    
    flash("Não foi possível adicionar nova categoria", "warning")
    return redirect(url_for("category_bp.category_index_page"))

@category_bp.route("/<int:category_id>/edit", methods=["POST"])
@login_required
def edit_category(category_id):
    new_name = request.form.get("category_name").capitalize()

    category = CategoryController.edit_category(category_id, new_name, current_user.id)

    if category:
        flash("Categoria editada com sucesso!", "success")
        return redirect(url_for("category_bp.category_index_page"))
    
    flash("Não foi possível editar a categoria", "warning")
    return redirect(url_for("category_bp.category_index_page"))

@category_bp.route("/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id):
    success = CategoryController.delete_category(category_id, current_user.id)

    if success:
        flash("Categoria deletada com sucesso!", "success")
        return redirect(url_for("category_bp.category_index_page"))
    
    flash("Não foi possível deletar a categoria", "warning")
    return redirect(url_for("category_bp.category_index_page"))