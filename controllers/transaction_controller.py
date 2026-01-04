from extensions import db
from models.transaction import Transaction
from models.wallet import Wallet
from models.category import UserCategory, SystemCategory
from utils.exceptions import CarteiraInexistenteError, SaldoInsuficienteError, CarteiraInexistenteError, ValorInvalidoError, TransacaoInexistenteError
from sqlalchemy import extract

class TransactionController():
    
    @staticmethod
    def create_transaction(transaction_type, value, wallet_id, category_id, user_id, description="", created_at=None):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValorInvalidoError("O valor da transação deve ser um número válido.")
        
        if value <= 0:
            raise ValorInvalidoError("O valor da transação deve ser maior que zero.")
        
        wallet = Wallet.query.filter_by(
            id= wallet_id, 
            user_id= user_id, 
            is_active= True).first()
        
        if not wallet:
            raise CarteiraInexistenteError("Carteira inexistente.")
        
        category = (
            UserCategory.query.filter_by(id= category_id, user_id= user_id).first()
            or
            SystemCategory.query.filter_by(id= category_id).first()            
        )

        if not category:
            raise CarteiraInexistenteError("Categoria inexistente.")

        # Saldo insuficiente
        if transaction_type == "expense" and wallet.current_balance < value:
            raise SaldoInsuficienteError("Saldo insuficiente na carteira para realizar esta despesa.")

        transaction = Transaction(
            transaction_type= transaction_type,
            value= value,
            wallet_id= wallet_id,
            category_id= category_id,
            description= description,
            created_at= created_at
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
        return Transaction.query.filter_by(wallet_id=wallet_id).order_by(Transaction.created_at.desc()).order_by(Transaction.id.desc()).all()

    @staticmethod
    def get_user_transactions(user_id, month, year):
        return Transaction.query.join(Wallet).filter(
            Wallet.user_id == user_id,
            extract("month", Transaction.created_at) == month,
            extract("year", Transaction.created_at) == year
        ).order_by(Transaction.created_at.desc()).order_by(Transaction.id.desc()).all()

    @staticmethod
    def delete_transaction(transaction_id, user_id):
        transaction = Transaction.query.filter_by(id= transaction_id).first()

        if not transaction:
            raise TransacaoInexistenteError("Transação inexistente.") 
        
        wallet = Wallet.query.filter_by(
            id= transaction.wallet_id,
            user_id= user_id,
            is_active= True
        ).first()

        if not wallet:
            raise CarteiraInexistenteError("Carteira inexistente.") 
        

        if transaction.transaction_type == "income":
            wallet.current_balance -= transaction.value
        else:
            wallet.current_balance += transaction.value

        db.session.delete(transaction)
        db.session.commit()

        return True

    @staticmethod
    def edit_transaction(transaction_id, value, created_at, description, category_id, user_id):
        transaction = Transaction.query.filter_by(id= transaction_id).first()

        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValorInvalidoError("O valor da transação deve ser um número válido.")

        if not transaction:
            raise TransacaoInexistenteError("Transação inexistente.")

        wallet_id = transaction.wallet_id

        wallet = Wallet.query.filter_by(
            id= wallet_id,
            user_id= user_id,
            is_active= True
        ).first()   

        if not wallet:
            raise CarteiraInexistenteError("Carteira inexistente.")
        
        if transaction.transaction_type == "income":
            wallet.current_balance -= transaction.value
        else:        
            wallet.current_balance += transaction.value

        if transaction.transaction_type == "expense" and wallet.current_balance < value:
            return False
        
        transaction.value = value
        transaction.created_at = created_at
        transaction.description = description
        transaction.category_id = category_id
        
        if transaction.transaction_type == "income":
            wallet.current_balance += transaction.value
        else:
            wallet.current_balance -= transaction.value  

        db.session.commit()
        return transaction