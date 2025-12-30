from extensions import db
from models.goal import Goal
from datetime import datetime

class GoalController():
    
    @staticmethod
    def create_goal(goal_name, target_amount, deadline, user_id, category_id=None):
        try:
            target_amount = float(target_amount)
        except:
            return None
        print("Existing Goal:")
        
        existing_goal = Goal.query.filter_by(
            user_id= user_id, 
            goal_name= goal_name
        ).first()


        if existing_goal and existing_goal.is_active:
            return None
        
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
    def verificar(user_id):
        goals = GoalController.get_goals_by_user(user_id)
        today = datetime.today().date()

        for goal in goals:
            if goal.deadline <= today:
                goal.is_active = False
                db.session.commit()