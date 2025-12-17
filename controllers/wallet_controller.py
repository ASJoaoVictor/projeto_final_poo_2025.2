from extensions import db
from models.wallet import Wallet
from models.category import SystemCategory
from controllers.transaction_controller import TransactionController
from controllers.category_controller import CategoryController


class WalletController():

    @staticmethod
    def create_wallet(wallet_name, initial_balance, user_id):
        try:
            initial_balance = float(initial_balance)
        except:
            return None
        
        existing_wallet = Wallet.query.filter_by(
            user_id= user_id, 
            wallet_name= wallet_name
        ).first()

        if existing_wallet and existing_wallet.is_active:
            return None
        
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
            return None

        if initial_balance > 0:
            TransactionController.create_transaction(
                transaction_type= "income",
                value= initial_balance,
                wallet_id= wallet.id,
                category_id= category.id,
                user_id= user_id,
            )

        return wallet
    
    @staticmethod
    def get_wallets_by_user(user_id):
        wallets = Wallet.query.filter_by(user_id= user_id, is_active= True).all()

        return wallets
    
    @staticmethod
    def get_wallet_by_id(wallet_id):
        wallet = Wallet.query.filter_by(id= wallet_id, is_active= True).first()

        return wallet

    @staticmethod
    def deactivate_wallet(wallet_id, user_id):
        wallet = Wallet.query.filter_by(
            id= wallet_id, 
            user_id= user_id).first()

        if not wallet:
            return None
        
        if wallet.current_balance > 0:
            TransactionController.create_transaction(
                transaction_type= "expense",
                value= wallet.current_balance,
                wallet_id= wallet.id,
                category_id= SystemCategory.query.filter_by(name= "Depósito inicial").first().id,
                user_id= user_id,
                description= "Fechamento de carteira"
            )

        wallet.is_active = False
        db.session.commit()
        return wallet
    
    @staticmethod
    def edit_wallet(wallet_id, new_name, new_initial_balance, user_id):
        wallet = Wallet.query.filter_by(
            id= wallet_id,
            user_id= user_id
        ).first()

        if not wallet:
            return None

        wallet.wallet_name = new_name
        db.session.commit()

        return wallet
