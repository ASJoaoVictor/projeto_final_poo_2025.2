from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.goal_controller import GoalController
from controllers.category_controller import CategoryController
from controllers.transaction_controller import TransactionController
from utils.exceptions import ValorInvalidoError, MetaJaExisteError, MetaInexistenteError

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goal")

@goal_bp.route("/", methods=["GET"])
@login_required
def goal_index_page():
    #Verificar prazos das metas
    GoalController.check_expired_goals(current_user.id)

    categories = CategoryController.get_user_categories(current_user.id)
    goals = GoalController.get_goals_by_user(current_user.id)

    goals_data = []

    for goal in goals:
        current_amount = 0
        if goal.category:
            for transaction in goal.category.transactions:
                if transaction.transaction_type == "expense" and transaction.created_at >= goal.created_at:
                    current_amount += transaction.value
        else:
            for transaction in TransactionController.get_user_transactions(current_user.id):
                if transaction.transaction_type == "expense" and transaction.created_at >= goal.created_at:
                    current_amount += transaction.value
        goals_data.append({
            'id': goal.id,
            'name': goal.goal_name,
            'category_name': goal.category.name if goal.category else 'Sem Categoria',
            'current': float(current_amount),
            'target': float(goal.target_amount),
            'percentage': min(int((current_amount / goal.target_amount) * 100), 100),
            'real_percentage': int((current_amount / goal.target_amount) * 100),
            'remaining': float(goal.target_amount - current_amount),
            'status': 'safe' if current_amount <= goal.target_amount * 0.8 else
                      'warning' if current_amount <= goal.target_amount else
                      'danger'
        })

    return render_template('goal/index.html', 
                           goals_data=goals_data,
                           categories=categories)

@goal_bp.route("/create", methods=["POST"])
@login_required
def create_goal():
    goal_name = request.form.get("goal_name").capitalize()
    target_amount = request.form.get("target_amount")
    category_id = request.form.get("category_id")
    user_id = current_user.id
    duration = request.form.get("duration")
    unit = request.form.get("unit")


    try:
        goal = GoalController.create_goal(goal_name, target_amount, user_id, duration, unit, category_id)
    except (ValorInvalidoError, MetaJaExisteError) as e:
        flash(str(e), "error")
        return redirect(url_for("goal_bp.goal_index_page"))
    except Exception as e:
        flash("Erro ao criar a meta. Tente novamente.", "error")
        print("Erro ao criar a meta:", e)
        return redirect(url_for("goal_bp.goal_index_page"))

    flash("Meta criada com sucesso!", "success")
    return redirect(url_for("goal_bp.goal_index_page"))

@goal_bp.route("/delete/<int:goal_id>", methods=["POST"])
@login_required
def delete_goal(goal_id):
    user_id = current_user.id

    try:
        GoalController.delete_goal(goal_id, user_id)
    except MetaInexistenteError as e:
        flash(str(e), "error")
        return redirect(url_for("goal_bp.goal_index_page"))
    except Exception as e:
        flash("Erro ao deletar a meta. Tente novamente.", "error")
        print("Erro ao deletar a meta:", e)
        return redirect(url_for("goal_bp.goal_index_page"))
    
    flash("Meta deletada com sucesso!", "success")
    return redirect(url_for("goal_bp.goal_index_page"))

@goal_bp.route("/edit/<int:goal_id>", methods=["POST"])
@login_required
def edit_goal(goal_id):
    user_id = current_user.id
    new_name = request.form.get("edit_goal_name").capitalize()
    new_target_amount = request.form.get("edit_target_amount")

    try:
        goal = GoalController.edit_goal(goal_id, user_id, new_name, new_target_amount)
    except (ValorInvalidoError, MetaJaExisteError, MetaInexistenteError) as e:
        flash(str(e), "error")
        return redirect(url_for("goal_bp.goal_index_page"))
    except Exception as e:
        flash("Erro ao editar a meta. Tente novamente.", "error")
        print("Erro ao editar a meta:", e)
        return redirect(url_for("goal_bp.goal_index_page"))
    
    flash("Meta editada com sucesso!", "success")
    return redirect(url_for("goal_bp.goal_index_page"))