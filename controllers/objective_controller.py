from extensions import db
from models.objective import Objective

class ObjectiveController():
    
    @staticmethod
    def create_objective(objective_name, target_amount, user_id, due_date=None):
        try:
            target_amount = float(target_amount)
        except:
            return None
        
        if target_amount <= 0:
            return None
        
        objective = Objective(
            objective_name= objective_name,
            target_amount= target_amount,
            user_id= user_id,
            due_date= due_date
        )

        db.session.add(objective)
        db.session.commit()

        return objective