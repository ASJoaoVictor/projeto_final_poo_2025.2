from extensions import db

class Objective(db.Model):
    __tablename__ = "objectives"

    id = db.Column(db.Integer, primary_key=True)
    objective_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    due_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    icon = db.Column(db.String(10), nullable=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Objective {self.objective_name}>"