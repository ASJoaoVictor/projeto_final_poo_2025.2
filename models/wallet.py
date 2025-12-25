from extensions import db
from datetime import datetime, timezone

class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key= True)
    wallet_name = db.Column(db.String(100), nullable= False)
    initial_balance = db.Column(db.Float, default= 0.0)
    current_balance = db.Column(db.Float, default= 0.0)
    is_active = db.Column(db.Boolean, default= True)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc).date())

    #chave FK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable= False)

    def __repr__(self):
        return f"<Wallet {self.wallet_name}>"