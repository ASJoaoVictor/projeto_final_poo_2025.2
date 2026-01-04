from extensions import db
from models.goal import Goal
from datetime import datetime, timedelta
from utils.exceptions import ValorInvalidoError, MetaJaExisteError, MetaInexistenteError

class GoalController():
    
    @staticmethod
    def create_goal(goal_name, target_amount, user_id, duration, unit, category_id=None):
        try:
            target_amount = float(target_amount)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Valor alvo inválido.")

        try:
            duration = int(duration)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Duração inválida.")
        
        real_unit = 1 if unit == "monthly" else 12
        duration_in_month = duration * real_unit
        deadline = datetime.now() + timedelta(days=30 * duration_in_month)
        
        existing_goal = Goal.query.filter_by(
            user_id= user_id, 
            goal_name= goal_name
        ).first()


        if existing_goal and existing_goal.is_active:
            raise MetaJaExisteError("Já existe uma meta ativa com esse nome.") 
        
        if existing_goal:
            goal = existing_goal
            goal.is_active = True
            goal.target_amount = target_amount
            goal.create_at = datetime.now().date
        else:
            goal = Goal(
                goal_name= goal_name,
                target_amount= target_amount,
                deadline= deadline,
                category_id= category_id,
                created_at= datetime.now().date(),
                user_id= user_id
            )

            db.session.add(goal)
            
        db.session.commit()

        return goal
    
    @staticmethod
    def get_goals_by_user(user_id):
        goals = Goal.query.filter_by(user_id= user_id, is_active= True).all()
        return goals

    @staticmethod
    def check_expired_goals(user_id):
        goals = GoalController.get_goals_by_user(user_id)
        today = datetime.today().date()

        for goal in goals:
            if goal.deadline <= today and goal.is_active:
                goal.is_active = False
        db.session.commit()

    @staticmethod
    def delete_goal(goal_id, user_id):
        goal = Goal.query.filter_by(
            id= goal_id,
            user_id= user_id,
            is_active= True
        ).first()

        if not goal:
            raise MetaInexistenteError("Meta inexistente.")
        
        db.session.delete(goal)
        #goal.is_active = False
        db.session.commit()

        return True
    
    @staticmethod
    def edit_goal(goal_id, user_id, new_name, new_target_amount):
        goal = Goal.query.filter_by(
            id= goal_id,
            user_id= user_id,
            is_active= True
        ).first()

        if not goal:
            raise MetaInexistenteError("Meta inexistente.")

        goal_existing = Goal.query.filter_by(
            user_id= user_id,
            goal_name= new_name
        ).first()

        if goal_existing and goal_existing.id != goal.id:
            raise MetaJaExisteError("Já existe uma meta ativa com esse nome.")
        
        try:
            new_target_amount = float(new_target_amount)
        except:
            raise ValorInvalidoError("Valor alvo inválido.")

        goal.goal_name = new_name
        goal.target_amount = new_target_amount
        db.session.commit()

        return goal