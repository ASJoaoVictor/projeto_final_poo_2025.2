from extensions import db
from datetime import datetime, timezone

class Transaction(db.Model):
    """Modelo de dados que representa uma movimentação financeira individual.

    Esta é a entidade central do sistema. Registra cada fluxo de entrada (income) 
    ou saída (expense) de dinheiro. Diferente de saldos que são calculados, 
    a transação é o registro histórico do fato.

    Regras de Negócio:
    - Toda transação DEVE pertencer a uma Carteira (`wallet_id`).
    - Toda transação DEVE ter uma Categoria (`category_id`).

    Attributes:
        id (int): Identificador único da transação (Primary Key).
        transaction_type (str): Define a natureza do movimento. Valores esperados:
                                'income' (Receita) ou 'expense' (Despesa).
        value (float): O valor monetário absoluto da transação.
        created_at (date): Data de competência da transação. Se não informada,
                           assume a data atual (UTC) automaticamente.
        description (str, optional): Um texto curto para detalhes extras (ex: 'Almoço no Shopping').
        
        wallet_id (int): Chave estrangeira da carteira afetada.
        category_id (int): Chave estrangeira da categoria que classifica este gasto/ganho.
        
        wallet (Wallet): Relacionamento ORM para acessar o objeto da carteira.
        category (Category): Relacionamento ORM para acessar o objeto da categoria.
    """
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key= True)
    transaction_type = db.Column(db.String(20), nullable= False)
    value = db.Column(db.Float, nullable= False)
    created_at = db.Column(db.Date, default= lambda: datetime.now(timezone.utc).date())
    description = db.Column(db.String(100), nullable= True)

    wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable= False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable= False)

    category = db.relationship("Category", backref= "transactions", lazy= True)
    wallet = db.relationship("Wallet", backref= "transactions", lazy= True)

    def __repr__(self):
        return f"<Transaction {self.transaction_type} ! {self.value}>"