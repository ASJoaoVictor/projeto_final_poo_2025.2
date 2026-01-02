from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from flask_login import login_required, current_user
from controllers.objective_controller import ObjectiveController
from controllers.category_controller import CategoryController
from controllers.wallet_controller import WalletController
from datetime import datetime, timedelta    

objective_bp = Blueprint("objective_bp", __name__, url_prefix="/objectives")

@objective_bp.route("/", methods=["GET"])
@login_required
def objective_index_page():
    wallets = WalletController.get_wallets_by_user(current_user.id)
    categories = CategoryController.get_user_categories(current_user.id)
    objectives = ObjectiveController.get_objectives_user(current_user.id)

    objectives_data = []
    for objective in objectives:
        if objective.wallet:
            current_balance = objective.wallet.current_balance
        else:
            current_balance = sum(wallet.current_balance for wallet in wallets)

        if objective.target_amount > 0:
            percentage = round((current_balance / objective.target_amount) * 100, 2)
        else:
            percentage = 0.0


        objectives_data.append({
            'id': objective.id,
            'objective_name': objective.objective_name,
            'objective_icon': objective.icon,
            'target_amount': objective.target_amount,
            'current_amount': current_balance,
            'due_date': objective.due_date,
            'percentage': percentage
        })

    return render_template('objective/index.html', 
                           objectives_data=objectives_data, 
                           categories=categories,
                           wallets=wallets)

@objective_bp.route("/create", methods=["POST"])
@login_required
def create_objective():
    objective_name = request.form.get("objective_name")
    target_amount = request.form.get("target_amount")
    wallet_id = request.form.get("wallet_id")
    icon = request.form.get("icon")
    due_date_str = request.form.get("due_date")

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Data de vencimento inválida.", "error")
            return redirect(url_for("objective_bp.objective_index_page"))

    objective = ObjectiveController.create_objective(
        objective_name=objective_name,
        target_amount=target_amount,
        user_id=current_user.id,
        icon=icon,
        wallet_id=wallet_id,
        due_date=due_date
    )

    if objective:
        flash("Objetivo criado com sucesso!", "success")
        return redirect(url_for("objective_bp.objective_index_page"))
    
    flash("Falha ao criar o objetivo. Verifique os dados fornecidos.", "error")
    return redirect(url_for("objective_bp.objective_index_page"))


@objective_bp.route("/delete/<int:objective_id>", methods=["POST"])
@login_required
def delete_objective(objective_id):
    success = ObjectiveController.delete_objective(objective_id)
    if success:
        flash("Objetivo deletado com sucesso!", "success")
        return redirect(url_for("objective_bp.objective_index_page"))
    
    flash("Objetivo não encontrado.", "error")
    return redirect(url_for("objective_bp.objective_index_page"))
