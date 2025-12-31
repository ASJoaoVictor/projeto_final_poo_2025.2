from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
from controllers.objective_controller import ObjectiveController
from flask_login import login_required, current_user
from datetime import datetime, timedelta    

objective_bp = Blueprint("objective_bp", __name__, url_prefix="/objectives")

@objective_bp.route("/", methods=["GET"])
@login_required
def objective_index_page():
    objectives_data = [
        {
            'id': 1,
            'objective_name': 'Viagem para Europa ✈️',
            'target_amount': 15000.00,
            'current_amount': 3450.00,
            'due_date': datetime.now() + timedelta(days=365), # Daqui a 1 ano
            'percentage': 23.0, 
        },
        {
            'id': 2,
            'objective_name': 'Macbook Pro 💻',
            'target_amount': 12000.00,
            'current_amount': 9600.00,
            'due_date': datetime.now() + timedelta(days=45), # Daqui a 45 dias
            'percentage': 80.0,
        },
        {
            'id': 3,
            'objective_name': 'Reserva de Emergência 🛡️',
            'target_amount': 10000.00,
            'current_amount': 10000.00, # Meta batida!
            'due_date': None, # Sem prazo definido
            'percentage': 100.0,
        },
        {
            'id': 4,
            'objective_name': 'Reforma do Quarto 🏠',
            'target_amount': 5000.00,
            'current_amount': 150.00, # Apenas começando
            'due_date': datetime.now() + timedelta(days=120),
            'percentage': 3.0,
        }
    ]
    
    return render_template('objective/index.html', objectives_data=objectives_data)