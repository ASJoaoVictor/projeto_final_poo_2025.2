from extensions import db

class Goal(db.Model):
    """Modelo de dados que representa uma Meta Financeira (Goal).

    No contexto deste sistema, uma Meta distingue-se de um Objetivo. Enquanto objetivos
    podem focar em conquistas materiais específicas, as Metas definem alvos financeiros
    atrelados a categorias ou prazos (ex: "Teto de gastos para Alimentação".

    Attributes:
        id (int): Identificador único da meta (Primary Key).
        goal_name (str): O nome descritivo da meta.
        target_amount (float): O valor alvo a ser respeitado.
        created_at (date): A data em que a meta foi estabelecida.
        is_active (bool): Flag que indica se a meta está vigente (True) ou encerrada (False).
        deadline (date, optional): A data limite para o cumprimento da meta.
        user_id (int): Chave estrangeira do usuário dono da meta.
        category_id (int, optional): Chave estrangeira que vincula esta meta a uma categoria específica.
        category (UserCategory): Relacionamento ORM para acessar os dados da categoria vinculada.
    """
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Date, nullable= False)
    is_active = db.Column(db.Boolean, default=True)

    #Prazo final
    deadline = db.Column(db.Date, nullable=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    category = db.relationship("UserCategory", backref="goals")

    def __repr__(self):
        return f"<Goal {self.goal_name}>"