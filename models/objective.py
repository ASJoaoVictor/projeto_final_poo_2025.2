from extensions import db

class Objective(db.Model):
    """Modelo de dados que representa um Objetivo Financeiro (Sonho/Aquisição).

    Diferente das Metas (Goals) que funcionam como tetos de gastos por categoria,
    os Objetivos representam conquistas materiais ou experiências específicas de 
    longo ou curto prazo (ex: 'Comprar Carro Novo', 'Viagem para Europa', 'PS5').

    Regra de Negócio:
    - O Objetivo pode ser vinculado a uma Carteira (`wallet_id`). Isso permite rastrear
      onde o dinheiro para este sonho está sendo acumulado (ex: uma conta de Investimento
      ou um 'Cofrinho' específico).

    Attributes:
        id (int): Identificador único do objetivo.
        objective_name (str): O título do objetivo.
        target_amount (float): O valor total necessário para realizar o objetivo.
        due_date (datetime, optional): A data planejada para a realização.
        is_active (bool): Flag de status. Se False, o objetivo foi concluído ou desistido.
        icon (str, optional): Um emoji ou código de ícone para representação visual no Dashboard.
        
        user_id (int): Chave estrangeira do usuário dono do objetivo.
        wallet_id (int, optional): Chave estrangeira da carteira onde os fundos estão alocados.
        
        user (User): Relacionamento ORM com o usuário.
        wallet (Wallet): Relacionamento ORM com a carteira vinculada.
    """
    __tablename__ = "objectives"

    id = db.Column(db.Integer, primary_key=True)
    objective_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    icon = db.Column(db.String(10), nullable=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id"), nullable=True)

    user = db.relationship("User", backref="objectives")
    wallet = db.relationship("Wallet", backref="objectives")

    def __repr__(self):
        return f"<Objective {self.objective_name}>"