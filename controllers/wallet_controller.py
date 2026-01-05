from extensions import db
from models.wallet import Wallet
from models.category import SystemCategory
from controllers.transaction_controller import TransactionController
from utils.exceptions import ValorInvalidoError, CarteiraJaExisteError, CategoriaInvalidaError, CarteiraInexistenteError, AcessoNegadoError

class WalletController():
    """Controlador responsável pelo gerenciamento de carteiras (Wallets) e seus saldos."""

    @staticmethod
    def create_wallet(wallet_name, initial_balance, user_id):
        """Cria uma nova carteira ou reativa uma antiga, gerando o saldo inicial.

        Se uma carteira com o mesmo nome já existir (mesmo inativa), ela é reativada.
        Caso o saldo inicial seja maior que zero, o sistema cria automaticamente uma
        transação de receita do tipo 'Depósito inicial'.

        Args:
            wallet_name (str): O nome da carteira (ex: 'Banco X', 'Cofre').
            initial_balance (float|str): O saldo inicial da carteira.
            user_id (int): O ID do usuário dono da carteira.

        Returns:
            Wallet: O objeto da carteira criada ou reativada.

        Raises:
            ValorInvalidoError: Se o saldo inicial não for numérico.
            CarteiraJaExisteError: Se já existir uma carteira ativa com esse nome.
            CategoriaInvalidaError: Se a categoria de sistema 'Depósito inicial' não for encontrada.
        """
        try:
            initial_balance = float(initial_balance)
        except (ValueError, TypeError):
            raise ValorInvalidoError("O valor inicial deve ser um número válido.")
        
        existing_wallet = Wallet.query.filter_by(
            user_id= user_id, 
            wallet_name= wallet_name
        ).first()

        if existing_wallet and existing_wallet.is_active:
            raise CarteiraJaExisteError("Já existe uma carteira com esse nome.") 
        
        if existing_wallet:
            wallet = existing_wallet
            wallet.is_active = True
            wallet.initial_balance = initial_balance
        else:
            wallet = Wallet(
                wallet_name= wallet_name,
                initial_balance= initial_balance,
                user_id= user_id
            )

            db.session.add(wallet)
            
        db.session.commit()

        category = SystemCategory.query.filter_by(name= "Depósito inicial").first()

        if not category:
            raise CategoriaInvalidaError("Categoria padrão 'Depósito inicial' não encontrada.")

        if initial_balance > 0:
            TransactionController.create_transaction(
                transaction_type= "income",
                value= initial_balance,
                wallet_id= wallet.id,
                category_id= category.id,
                user_id= user_id,
                description= "Depósito para abertura"
            )

        return wallet
    
    @staticmethod
    def get_wallets_by_user(user_id):
        """Recupera todas as carteiras ativas de um usuário.

        Args:
            user_id (int): O ID do usuário.

        Returns:
            list[Wallet]: Lista de objetos Wallet ativos.
        """
        wallets = Wallet.query.filter_by(user_id= user_id, is_active= True).all()

        return wallets
    
    @staticmethod
    def get_wallet_by_id(wallet_id, user_id):
        """Busca uma carteira específica pelo ID e verifica se pertence ao usuário.

        Args:
            wallet_id (int): O ID da carteira.
            user_id (int): O ID do usuário.

        Returns:
            Wallet: O objeto da carteira encontrada.

        Raises:
            CarteiraInexistenteError: Se a carteira não for encontrada ou não estiver ativa.
        """
        wallet = Wallet.query.filter_by(id= wallet_id, user_id= user_id, is_active= True).first()

        if not wallet:
            raise CarteiraInexistenteError("Carteira não encontrada.")
            
        return wallet

    @staticmethod
    def deactivate_wallet(wallet_id, user_id):
        """Desativa uma carteira (Soft Delete) sem excluir seus dados.

        Busca a carteira pelo ID e usuário, e define a flag 'is_active' como False.

        Args:
            wallet_id (int): O ID da carteira.
            user_id (int): O ID do usuário.

        Returns:
            Wallet: A carteira atualizada.

        Raises:
            CarteiraInexistenteError: Se a carteira não for encontrada.
        """
        wallet = Wallet.query.filter_by(
            id= wallet_id, 
            user_id= user_id).first()

        if not wallet:
            raise CarteiraInexistenteError("Carteira não encontrada.")

        wallet.is_active = False
        db.session.commit()
        return wallet

    @staticmethod  
    def delete_wallet(wallet_id, user_id):
        """Exclui permanentemente uma carteira e todas as suas transações (Hard Delete).

        Busca a carteira validando a propriedade pelo usuário. Realiza uma exclusão em cascata:
        remove todas as transações vinculadas antes de deletar a carteira do banco de dados.

        Args:
            wallet_id (int): O ID da carteira a ser excluída.
            user_id (int): O ID do usuário solicitante.

        Returns:
            bool: Retorna True se a exclusão for bem-sucedida.

        Raises:
            CarteiraInexistenteError: Se a carteira não for encontrada ou não pertencer ao usuário.
        """
        wallet = WalletController.get_wallet_by_id(wallet_id, user_id)

        if not wallet:
            raise CarteiraInexistenteError("Carteira não encontrada.")
        
        transactions = TransactionController.get_transactions_by_wallet(wallet_id)

        for transaction in transactions:
            TransactionController.delete_transaction(transaction.id, user_id) # deleta todas as transações da carteira

        db.session.delete(wallet)
        db.session.commit()

        return True
    
    @staticmethod
    def edit_wallet(wallet_id, new_name, user_id):
        """Renomeia uma carteira existente.

        Verifica duplicidade de nomes antes de aplicar a alteração.

        Args:
            wallet_id (int): O ID da carteira a ser editada.
            new_name (str): O novo nome desejado.
            user_id (int): O ID do usuário.

        Returns:
            Wallet: A carteira atualizada.

        Raises:
            CarteiraInexistenteError: Se a carteira não for encontrada.
            CarteiraJaExisteError: Se o usuário já tiver outra carteira com o novo nome.
        """
        wallet = Wallet.query.filter_by(
            id= wallet_id,
            user_id= user_id
        ).first()

        if not wallet:
            raise CarteiraInexistenteError("Carteira não encontrada.")

        wallet_existing = Wallet.query.filter_by(
            user_id= user_id,
            wallet_name= new_name
        ).first()

        if wallet_existing and wallet_existing.id != wallet_id:
            raise CarteiraJaExisteError("Já existe uma carteira com esse nome.") 

        wallet.wallet_name = new_name
        db.session.commit()

        return wallet
