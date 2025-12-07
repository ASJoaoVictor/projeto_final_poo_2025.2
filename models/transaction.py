from extensions import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key= True)
    transaction_type = db.Column(db.String(20), nullable= False)
    value = db.Column(db.Float, nullable= False)
    #create_at = db.Column(db) colocar no futuro

    wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable= False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable= False)

    category = db.relationship("Category", lazy= True)

    def __repr__(self):
        return f"<Transaction {self.transaction_type} ! {self.value}>"