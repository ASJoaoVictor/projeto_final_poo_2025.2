from extensions import db
from datetime import datetime, timezone

class Wallet(db.Model):
    """Modelo de dados que representa uma Carteira (Fonte de Recursos).

    As carteiras são os 'contêineres' de dinheiro do usuário. Podem representar
    contas bancárias, dinheiro em espécie (físico), corretoras de investimento 
    ou até contas poupança.

    O sistema rastreia dois estados de saldo:
    1. O ponto de partida (`initial_balance`).
    2. O estado atual (`current_balance`), que deve flutuar conforme transações ocorrem.

    Attributes:
        id (int): Identificador único da carteira.
        wallet_name (str): Nome identificador (ex: 'Nubank', 'Cofre', 'Investimentos').
        initial_balance (float): O saldo existente no momento do cadastro da carteira. 
                                 Geralmente estático após a criação.
        current_balance (float): O saldo atualizado em tempo real.
                                 ATENÇÃO: Este campo deve ser recalculado ou atualizado 
                                 sempre que uma transação de receita/despesa for realizada.
        is_active (bool): Flag de 'Soft Delete'. Se False, a carteira é arquivada.
        created_at (datetime): Data de registro da carteira.
        user_id (int): Chave estrangeira do usuário proprietário.
    """
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key= True)
    wallet_name = db.Column(db.String(100), nullable= False)
    initial_balance = db.Column(db.Float, default= 0.0)
    current_balance = db.Column(db.Float, default= 0.0)
    is_active = db.Column(db.Boolean, default= True)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc).date())

    #chave FK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable= False)

    def __repr__(self):
        return f"<Wallet {self.wallet_name}>"