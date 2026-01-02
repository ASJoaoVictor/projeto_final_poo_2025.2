from extensions import db

class Objective(db.Model):
    __tablename__ = "objectives"

    id = db.Column(db.Integer, primary_key=True)
    objective_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    icon = db.Column(db.String(10), nullable=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=True)

    user = db.relationship("User", backref="objectives")
    wallet = db.relationship("Wallet", backref="objectives")

    def __repr__(self):
        return f"<Objective {self.objective_name}>"