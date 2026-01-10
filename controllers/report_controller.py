from sqlalchemy import func, extract
from extensions import db
from models.transaction import Transaction
from models.category import Category
from models.wallet import Wallet

class ReportController:
    """Controlador responsável pela geração de relatórios e agregação de dados financeiros."""
    
    @staticmethod
    def get_expenses_by_category(user_id, month, year):
        """Retorna os gastos agrupados por categoria para um mês e ano específicos.

        Realiza uma consulta agregada no banco de dados que soma o valor das transações 
        do tipo 'despesa', agrupando-as pelo nome da categoria. Garante que apenas 
        transações de carteiras pertencentes ao usuário sejam consideradas.

        Args:
            user_id (int): O ID do usuário para filtrar os dados.
            month (int): O mês numérico (1-12) para o filtro.
            year (int): O ano (ex: 2026) para o filtro.

        Returns:
            list[tuple]: Uma lista de tuplas onde cada tupla contém (Nome da Categoria, Valor Total).
                         Exemplo: [('Alimentação', 500.00), ('Transporte', 150.00)].
                         Retorna uma lista vazia [] se não houver dados.
        """

        results = db.session.query(Category.name, func.sum(Transaction.value))\
            .join(Category, Transaction.category_id == Category.id)\
            .join(Wallet, Transaction.wallet_id == Wallet.id)\
            .filter(Wallet.user_id == user_id)\
            .filter(Transaction.transaction_type == 'expense')\
            .filter(extract('month', Transaction.created_at) == month)\
            .filter(extract('year', Transaction.created_at) == year)\
            .group_by(Category.name)\
            .all()
            
        return results if results else []

    @staticmethod
    def get_monthly_summary(user_id, month, year):
        """"Gera um resumo consolidado de Receitas, Despesas e Saldo do mês (RF9.2).

        Busca todas as transações do período especificado e calcula os totais em memória.
        O saldo mensal é calculado aritmeticamente (Total Receitas - Total Despesas),
        representando o fluxo de caixa do mês, independente do saldo acumulado nas carteiras.

        Args:
            user_id (int): O ID do usuário dono das transações.
            month (int): O mês de referência.
            year (int): O ano de referência.

        Returns:
            dict: Um dicionário contendo as chaves:
                - "income" (float): Total de entradas no mês.
                - "expense" (float): Total de saídas no mês.
                - "balance" (float): Saldo resultante do período (Receita - Despesa).
        """
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
        """Calcula o patrimônio total somando o saldo atual de todas as carteiras (RF9.3).

        Esta função oferece um "snapshot" da riqueza atual do usuário. Considera apenas 
        carteiras marcadas como ativas (`is_active=True`).

        Args:
            user_id (int): O ID do usuário.

        Returns:
            float: A soma total dos saldos das carteiras. 
                   Retorna 0.0 se o usuário não tiver carteiras ou saldo.
        """
        result = db.session.query(func.sum(Wallet.current_balance))\
            .filter(Wallet.user_id == user_id, Wallet.is_active == True)\
            .scalar() # scalar() retorna um único valor
            
        return result if result else 0.0