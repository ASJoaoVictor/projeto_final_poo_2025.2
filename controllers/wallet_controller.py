from extensions import db
from models.wallet import Wallet

class WalletController():

    @staticmethod
    def create_wallet(wallet_name, initial_balance, user_id):
        initial_balance = float(initial_balance)
        
        existing_wallet = Wallet.query.filter_by(user_id= user_id, wallet_name= wallet_name).first()

        if existing_wallet:
            return None

        wallet = Wallet(
            wallet_name= wallet_name,
            initial_balance= initial_balance,
            user_id= user_id
        )

        db.session.add(wallet)
        db.session.commit()

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
        wallet = Wallet.query.filter_by(id= wallet_id, user_id= user_id).first()

        if not wallet:
            return None
        
        wallet.is_active = False
        db.session.commit()

        return wallet
