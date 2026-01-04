from extensions import db
from models.objective import Objective
from utils.exceptions import ValorInvalidoError, ObjetivoInexistenteError

class ObjectiveController():
    
    @staticmethod
    def create_objective(objective_name, target_amount, user_id, icon, wallet_id, due_date=None):
        try:
            target_amount = float(target_amount)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Valor inválido para o objetivo.")
        
        if target_amount <= 0:
            raise ValorInvalidoError("O valor do objetivo deve ser positivo.")

        objective = Objective(
            objective_name= objective_name,
            target_amount= target_amount,
            due_date= due_date,
            user_id= user_id,
            wallet_id= wallet_id,
            icon = icon
        )

        db.session.add(objective)
        db.session.commit()

        return objective

    @staticmethod
    def get_objectives_user(user_id):
        return Objective.query.filter_by(user_id=user_id, is_active=True).all()

    @staticmethod
    def delete_objective(objective_id):
        objective = Objective.query.get(objective_id)

        if not objective:
            raise ObjetivoInexistenteError("Objetivo não encontrado.")

        db.session.delete(objective)
        db.session.commit()
        return True

    @staticmethod
    def edit_objective(id, new_name, new_target_amount, new_due_date, new_icon, new_wallet_id):
        objective = Objective.query.get(id)
        if not objective:
            raise ObjetivoInexistenteError("Objetivo não encontrado.")
        
        try:
            new_target_amount = float(new_target_amount)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Valor inválido para o objetivo.")
        
        if new_target_amount <= 0:
            raise ValorInvalidoError("O valor do objetivo deve ser positivo.")

        objective.objective_name = new_name
        objective.target_amount = new_target_amount
        objective.due_date = new_due_date
        objective.icon = new_icon
        objective.wallet_id = new_wallet_id

        db.session.commit()
        return objective