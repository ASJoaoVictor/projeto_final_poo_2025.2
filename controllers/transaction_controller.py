from extensions import db
from models.transaction import Transaction
from models.wallet import Wallet
from models.category import UserCategory, SystemCategory
from utils.exceptions import CarteiraInexistenteError, SaldoInsuficienteError, CarteiraInexistenteError, ValorInvalidoError, TransacaoInexistenteError
from sqlalchemy import extract

class TransactionController():
    """Controlador responsável pelo gerenciamento de transações financeiras (receitas e despesas)."""
    
    @staticmethod
    def create_transaction(transaction_type, value, wallet_id, category_id, user_id, description="", created_at=None):
        """Cria uma nova transação e atualiza o saldo da carteira correspondente.

        Verifica a existência da carteira e da categoria (seja do sistema ou do usuário).
        Se for uma despesa, verifica se há saldo suficiente. Após a criação,
        o saldo da carteira é ajustado (somado para receitas, subtraído para despesas).

        Args:
            transaction_type (str): Tipo da transação ("income" ou "expense").
            value (float|str): O valor monetário da transação.
            wallet_id (int): O ID da carteira onde a transação ocorrerá.
            category_id (int): O ID da categoria associada.
            user_id (int): O ID do usuário dono da transação.
            description (str, optional): Descrição opcional da transação.
            created_at (datetime, optional): Data da transação. Se None, usa data atual.

        Returns:
            Transaction: O objeto da transação criada.

        Raises:
            ValorInvalidoError: Se o valor for inválido ou menor/igual a zero.
            CarteiraInexistenteError: Se a carteira ou categoria não forem encontradas.
            SaldoInsuficienteError: Se for uma despesa e a carteira não tiver saldo.
        """
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
        """Recupera todas as transações de uma carteira específica.

        Args:
            wallet_id (int): O ID da carteira.

        Returns:
            list[Transaction]: Lista de transações ordenadas por data (mais recentes primeiro).
        """
        return Transaction.query.filter_by(wallet_id=wallet_id).order_by(Transaction.created_at.desc()).order_by(Transaction.id.desc()).all()

    @staticmethod
    def get_user_transactions(user_id, month=None, year=None):
        """Recupera o histórico de transações de um usuário.

        Se mês e ano forem fornecidos, retorna as transações daquele período específico.
        Caso contrário (se mês ou ano não forem informados), retorna todo o histórico 
        de transações do usuário, sem filtro de data.

        Args:
            user_id (int): O ID do usuário.
            month (int, optional): O mês numérico (1-12). Se None, retorna todas as transações.
            year (int, optional): O ano com 4 dígitos. Se None, retorna todas as transações.

        Returns:
            list[Transaction]: Lista de transações ordenadas por data (mais recentes primeiro).
        """
        if month is None or year is None:
            return Transaction.query.join(Wallet).filter(
                Wallet.user_id == user_id
            ).order_by(Transaction.created_at.desc()).order_by(Transaction.id.desc()).all()
        
        return Transaction.query.join(Wallet).filter(
            Wallet.user_id == user_id,
            extract("month", Transaction.created_at) == month,
            extract("year", Transaction.created_at) == year
        ).order_by(Transaction.created_at.desc()).order_by(Transaction.id.desc()).all()

    @staticmethod
    def delete_transaction(transaction_id, user_id):
        """Exclui uma transação e reverte o impacto no saldo da carteira.

        Se a transação excluída era uma receita, o valor é subtraído da carteira.
        Se era uma despesa, o valor é devolvido (somado) à carteira.

        Args:
            transaction_id (int): O ID da transação a ser excluída.
            user_id (int): O ID do usuário (para validação de segurança).

        Returns:
            bool: Retorna True se a exclusão for bem-sucedida.

        Raises:
            TransacaoInexistenteError: Se a transação não for encontrada.
            CarteiraInexistenteError: Se a carteira vinculada não for encontrada ou não pertencer ao usuário.
        """
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
        """Edita uma transação existente e recalcula o saldo da carteira.

        A função reverte o impacto da transação original no saldo da carteira,
        verifica se há fundos suficientes para o novo valor (caso seja despesa)
        e aplica as alterações.

        Args:
            transaction_id (int): O ID da transação a ser editada.
            value (float|str): O novo valor da transação.
            created_at (datetime): A nova data da transação.
            description (str): A nova descrição.
            category_id (int): O novo ID da categoria.
            user_id (int): O ID do usuário (para validação de segurança).

        Returns:
            Transaction: O objeto Transaction atualizado com os novos dados.

        Raises:
            ValorInvalidoError: Se o novo valor não for numérico.
            TransacaoInexistenteError: Se a transação não for encontrada.
            CarteiraInexistenteError: Se a carteira vinculada não for encontrada ou não pertencer ao usuário.
            SaldoInsuficienteError: Se a alteração resultar em saldo negativo na carteira (apenas para despesas).
        """
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
            raise SaldoInsuficienteError("Saldo insuficiente na carteira para realizar esta despesa.")
        
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