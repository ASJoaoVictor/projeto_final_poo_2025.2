from extensions import db
from models.wallet import Wallet
from models.category import SystemCategory
from controllers.transaction_controller import TransactionController
from utils.exceptions import ValorInvalidoError, CarteiraJaExisteError, CategoriaInvalidaError, CarteiraInexistenteError, AcessoNegadoError
class WalletController():

    @staticmethod
    def create_wallet(wallet_name, initial_balance, user_id):
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
        wallets = Wallet.query.filter_by(user_id= user_id, is_active= True).all()

        return wallets
    
    @staticmethod
    def get_wallet_by_id(wallet_id, user_id):
        wallet = Wallet.query.filter_by(id= wallet_id, user_id= user_id, is_active= True).first()

        if not wallet:
            raise CarteiraInexistenteError("Carteira não encontrada.")
            
        return wallet

    @staticmethod
    def deactivate_wallet(wallet_id, user_id):
        wallet = Wallet.query.filter_by(
            id= wallet_id, 
            user_id= user_id).first()

        if not wallet:
            return None

        wallet.is_active = False
        db.session.commit()
        return wallet

    @staticmethod  
    def delete_wallet(wallet_id, user_id):
        wallet = WalletController.get_wallet_by_id(wallet_id)

        if not wallet:
            raise CarteiraInexistenteError("Carteira não encontrada.")
        
        if wallet.user_id != user_id:
            raise AcessoNegadoError("Acesso negado à carteira.") 
        
        transactions = TransactionController.get_transactions_by_wallet(wallet_id)

        for transaction in transactions:
            TransactionController.delete_transaction(transaction.id, user_id) # deleta todas as transações da carteira

        db.session.delete(wallet)
        db.session.commit()

        return wallet
    
    @staticmethod
    def edit_wallet(wallet_id, new_name, user_id):
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
