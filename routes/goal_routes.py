from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goal")

@goal_bp.route("/", methods=["GET"])
def goal_index_page():
# --- DADOS FICTÍCIOS (MOCK) ---
    # Simulando o que viria do banco de dados jpa calculado
    goals_data = [
        {
            'name': 'Economia Mercado',
            'category_name': 'Alimentação',
            'current': 450.00,
            'target': 1000.00,
            'percentage': 45,       # (450/1000) * 100
            'real_percentage': 45,
            'remaining': 550.00,
            'status': 'safe'        # Verde
        },
        {
            'name': 'Limitar Ifood e Pizza',
            'category_name': 'Lazer',
            'current': 480.00,
            'target': 500.00,
            'percentage': 96,
            'real_percentage': 96,
            'remaining': 20.00,
            'status': 'warning'     # Amarelo (perto de estourar)
        },
        {
            'name': 'Combustível do Mês',
            'category_name': 'Transporte',
            'current': 350.00,
            'target': 300.00,
            'percentage': 100,      # A barra visual trava em 100%
            'real_percentage': 116, # O valor real passou
            'remaining': -50.00,    # Negativo
            'status': 'danger'      # Vermelho
        }
    ]

    return render_template('goal/index.html', goals_data=goals_data)