from extensions import db

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Date, nullable= False)
    is_active = db.Column(db.Boolean, default=True)

    #Prazo final
    deadline = db.Column(db.Date, nullable=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    category = db.relationship("UserCategory", backref="goals")

    def __repr__(self):
        return f"<Goal {self.goal_name}>"