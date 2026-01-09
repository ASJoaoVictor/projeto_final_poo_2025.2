from sqlalchemy import func, extract
from extensions import db
from models.transaction import Transaction
from models.category import Category
from models.wallet import Wallet

class ReportController:
    
    @staticmethod
    def get_expenses_by_category(user_id, month, year):
        """RF9.1: Retorna gastos agrupados por categoria para o mês/ano."""
        
        # Query: Soma o valor das transações, agrupando pelo nome da categoria
        # AJUSTE: Adicionado .join(Wallet) e filtro por Wallet.user_id
        results = db.session.query(Category.name, func.sum(Transaction.value))\
            .join(Category, Transaction.category_id == Category.id)\
            .join(Wallet, Transaction.wallet_id == Wallet.id)\
            .filter(Wallet.user_id == user_id)\
            .filter(Transaction.transaction_type == 'expense')\
            .filter(extract('month', Transaction.created_at) == month)\
            .filter(extract('year', Transaction.created_at) == year)\
            .group_by(Category.name)\
            .all()
            
        # Retorna lista de tuplas: [('Alimentação', 500.00), ('Lazer', 200.00)]
        return results if results else []

    @staticmethod
    def get_monthly_summary(user_id, month, year):
        """RF9.2: Retorna totais de Receita, Despesa e Saldo do mês."""
        
        # AJUSTE: Transaction.query.join(Wallet) para filtrar pelo dono da carteira
        transactions = Transaction.query\
            .join(Wallet, Transaction.wallet_id == Wallet.id)\
            .filter(Wallet.user_id == user_id)\
            .filter(extract('month', Transaction.created_at) == month)\
            .filter(extract('year', Transaction.created_at) == year)\
            .all()

        total_income = sum(t.value for t in transactions if t.transaction_type == 'income')
        total_expense = sum(t.value for t in transactions if t.transaction_type == 'expense')
        
        # O saldo aqui é puramente matemático do mês (Receita - Despesa)
        monthly_balance = total_income - total_expense

        return {
            "income": total_income,
            "expense": total_expense,
            "balance": monthly_balance
        }

    @staticmethod
    def get_consolidated_wallet_balance(user_id):
        """RF9.3: Soma o saldo atual de TODAS as carteiras ativas."""
        
        # Aqui não precisa de ajuste, pois Wallet tem user_id direto
        result = db.session.query(func.sum(Wallet.current_balance))\
            .filter(Wallet.user_id == user_id, Wallet.is_active == True)\
            .scalar() # scalar() retorna um único valor
            
        return result if result else 0.0