from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from controllers.category_controller import CategoryController
from utils.exceptions import CategoriaJaExisteError, CarteiraInexistenteError

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

    try:
        category = CategoryController.create_category(category_name, current_user.id)
    except CategoriaJaExisteError as e:
        flash(str(e), "warning")
        return redirect(url_for("category_bp.category_index_page"))
    except Exception as e:
        flash("Erro ao criar categoria, tente novamente.", "error")
        print("Error ao criar categoria:", e)
        return redirect(url_for("category_bp.category_index_page"))

    flash("Nova categoria adicionada com sucesso!", "success")
    return redirect(url_for("category_bp.category_index_page"))

@category_bp.route("/<int:category_id>/edit", methods=["POST"])
@login_required
def edit_category(category_id):
    new_name = request.form.get("category_name").capitalize()

    try:
        category = CategoryController.edit_category(category_id, new_name, current_user.id)
    except CarteiraInexistenteError as e:
        flash(str(e), "warning")
        return redirect(url_for("category_bp.category_index_page"))
    except Exception as e:
        flash("Erro ao editar categoria, tente novamente.", "error")
        print("Error ao editar categoria:", e)
        return redirect(url_for("category_bp.category_index_page"))

    flash("Categoria editada com sucesso!", "success")
    return redirect(url_for("category_bp.category_index_page"))

@category_bp.route("/<int:category_id>/delete", methods=["POST"])
@login_required
def delete_category(category_id):

    try: 
        CategoryController.delete_category(category_id, current_user.id)
    except CarteiraInexistenteError as e:
        flash(str(e), "warning")
        return redirect(url_for("category_bp.category_index_page"))
    except Exception as e:
        flash("Erro ao deletar categoria, tente novamente.", "warning")
        print("Error ao deletar categoria:", e)
        return redirect(url_for("category_bp.category_index_page"))

    flash("Categoria deletada com sucesso!", "success")
    return redirect(url_for("category_bp.category_index_page"))