from flask import Blueprint, render_template, request, jsonify
from controllers.report_controller import ReportController
from datetime import datetime
from flask_login import login_required, current_user
# Importe o ReportController criado acima

report_bp = Blueprint('report_bp', __name__, url_prefix='/teste')

@report_bp.route("/", methods=["GET"])
def report_page():
    today = datetime.now()
    
    # Filtros da URL (ou padrão mês atual)
    selected_month = request.args.get("month", today.month, type=int)
    selected_year = request.args.get("year", today.year, type=int)

    # 1. Dados Consolidados (RF9.3)
    total_patrimony = ReportController.get_consolidated_wallet_balance(current_user.id)

    # 2. Resumo Mensal (RF9.2)
    monthly_summary = ReportController.get_monthly_summary(current_user.id, selected_month, selected_year)

    # 3. Dados por Categoria (RF9.1)
    category_data = ReportController.get_expenses_by_category(current_user.id, selected_month, selected_year)
    
    # Prepara dados para o Chart.js (separa labels e values)
    cat_labels = [row[0] for row in category_data] # Nomes das categorias
    cat_values = [row[1] for row in category_data] # Valores somados

    return render_template("report/index.html",
                           total_patrimony=total_patrimony,
                           monthly_summary=monthly_summary,
                           cat_labels=cat_labels,
                           cat_values=cat_values,
                           selected_month=selected_month,
                           selected_year=selected_year)