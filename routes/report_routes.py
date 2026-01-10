from flask import Blueprint, render_template, request, jsonify
from controllers.report_controller import ReportController
from datetime import datetime
from flask_login import login_required, current_user

report_bp = Blueprint('report_bp', __name__, url_prefix='/teste')

@report_bp.route("/", methods=["GET"])
def report_page():
    """Exibe a página principal de relatórios financeiros.

    Esta rota atua como um orquestrador, coletando filtros da requisição HTTP e 
    buscando os dados consolidados no `ReportController` para alimentar a interface.

    Processos realizados:
    1. Captura filtros de Mês/Ano da URL (padrão: data atual).
    2. Busca Patrimônio Total acumulado.
    3. Busca Resumo Mensal de Entradas/Saídas.
    4. Busca e formata dados de Categorias para renderização no Chart.js.

    Query Params:
        month (int, optional): O mês para filtragem (1-12). Default: Mês atual.
        year (int, optional): O ano para filtragem (ex: 2026). Default: Ano atual.

    Returns:
        str: O template HTML renderizado ('report/index.html') com o contexto 
             necessário para popular os cards e gráficos.
    """
    today = datetime.now()
    
    # Filtros da URL (ou padrão mês atual)
    selected_month = request.args.get("month", today.month, type=int)
    selected_year = request.args.get("year", today.year, type=int)

    # 1. Dados Consolidados
    total_patrimony = ReportController.get_consolidated_wallet_balance(current_user.id)

    # 2. Resumo Mensal
    monthly_summary = ReportController.get_monthly_summary(current_user.id, selected_month, selected_year)

    # 3. Dados por Categoria
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