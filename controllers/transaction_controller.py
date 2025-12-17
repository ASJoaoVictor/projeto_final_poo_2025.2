from extensions import db
from models.transaction import Transaction
from models.wallet import Wallet
from models.category import UserCategory, SystemCategory

class TransactionController():
    
    @staticmethod
    def create_transaction(transaction_type, value, wallet_id, category_id, user_id, description=None, created_at=None):
        try:
            value = float(value)
        except:
            return None
        
        if value <= 0:
            return None
        
        wallet = Wallet.query.filter_by(
            id= wallet_id, 
            user_id= user_id, 
            is_active= True).first()
        
        if not wallet:
            return None
        
        category = (
            UserCategory.query.filter_by(id= category_id, user_id= user_id).first()
            or
            SystemCategory.query.filter_by(id= category_id).first()            
        )

        if not category:
            return None

        # Saldo insuficiente
        if transaction_type == "expense" and wallet.current_balance < value:
            return None

        transaction = Transaction(
            transaction_type= transaction_type,
            value= value,
            wallet_id= wallet_id,
            category_id= category_id,
            description= description,
            #created_at= created_at
        )

        if transaction_type == "income":
            wallet.current_balance += value
        else:
            wallet.current_balance -= value

        db.session.add(transaction)
        db.session.commit()

        return transaction
            

    @staticmethod
    def get_transactions_by_wallet(wallet_id):
        # Mudamos de .asc() para .desc()
        print(Transaction.query.filter_by(wallet_id=wallet_id).order_by(Transaction.created_at.desc()).all())
        return Transaction.query.filter_by(wallet_id=wallet_id).order_by(Transaction.created_at.desc()).all()

    @staticmethod
    def get_transactions_by_user(user_id):
        pass