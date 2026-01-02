from extensions import db
from models.objective import Objective

class ObjectiveController():
    
    @staticmethod
    def create_objective(objective_name, target_amount, user_id, icon, wallet_id, due_date=None):
        try:
            target_amount = float(target_amount)
        except:
            return None
        
        if target_amount <= 0:
            return None
        
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
        if objective:
            db.session.delete(objective)
            db.session.commit()
            return True
        return False